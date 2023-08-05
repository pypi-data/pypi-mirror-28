#!/usr/bin/env python3
#
# This file is part of sarracenia.
# The sarracenia suite is Free and is proudly provided by the Government of Canada
# Copyright (C) Her Majesty The Queen in Right of Canada, Environment Canada, 2008-2015
#
# Questions or bugs report: dps-client@ec.gc.ca
# sarracenia repository: git://git.code.sf.net/p/metpx/git
# Documentation: http://metpx.sourceforge.net/#SarraDocumentation
#
# sr_consumer.py : python3 wraps consumer queue binding accept/reject
#
# Code contributed by:
#  Michel Grenier - Shared Services Canada
#  first shot     : Dec 11 10:26:22 EST 2015
#
########################################################################
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful, 
#  but WITHOUT ANY WARRANTY; without even the implied warranty of 
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA
#

import os,json,sys,random,time

try :    
         from sr_amqp           import *
         from sr_config         import *
         from sr_message        import *
         from sr_util           import *
except : 
         from sarra.sr_amqp     import *
         from sarra.sr_config   import *
         from sarra.sr_message  import *
         from sarra.sr_util     import *

# class sr_consumer

class sr_consumer:

    def __init__(self, parent, admin=False ):
        self.logger         = parent.logger
        self.logger.debug("sr_consumer __init__")
        self.parent         = parent

        self.retry_fp       = None
        self.retry_addmode  = False
        self.retry_getmode  = False

        if admin : return

        self.use_pattern    = parent.masks != []
        self.accept_unmatch = parent.accept_unmatch
        self.save = False

        self.iotime = 30
        if self.parent.timeout : self.iotime = int(self.parent.timeout)

        # truncated exponential backoff for consume...

        self.sleep_max = 1
        self.sleep_min = 0.01
        self.sleep_now = self.sleep_min

        self.build_connection()
        self.build_consumer()
        self.build_queue()
        self.get_message()

    def build_connection(self):
        self.logger.debug("sr_consumer build_broker")

        self.broker     = self.parent.broker

        self.logger.info("AMQP  broker(%s) user(%s) vhost(%s)" % \
                        (self.broker.hostname,self.broker.username,self.broker.path) )

        self.hc = HostConnect( logger = self.logger )
        self.hc.set_pika(self.parent.use_pika)
        self.hc.set_url(self.broker)
        self.hc.connect()

    def build_consumer(self):
        self.logger.debug("sr_consumer build_consumer")

        self.consumer = Consumer(self.hc)

        if self.parent.prefetch > 0 :
            self.consumer.add_prefetch(self.parent.prefetch)

        self.consumer.build()

        self.retry_msg = self.consumer.retry_msg
    def build_queue(self):
        self.logger.debug("sr_consumer build_queue")

        self.broker      = self.parent.broker
        self.bindings    = self.parent.bindings

        self.broker_str  = self.broker.geturl().replace(':'+self.broker.password+'@','@')

        # queue name 
        self.queue_declare(build=False)

        # queue bindings 

        for tup in self.bindings :
            exchange, key = tup
            self.logger.info('Binding queue %s with key %s from exchange %s on broker %s' % \
		            ( self.queue_name, key, exchange, self.broker_str ) )
            self.msg_queue.add_binding( exchange, key )

        # queue creation 
        self.msg_queue.build()

    def close(self):
        self.hc.close()

    def consume(self):

        # acknowledge last message... we are done with it since asking for a new one
        if self.raw_msg != None and not self.raw_msg.isRetry : self.consumer.ack(self.raw_msg)

        # consume a new one
        self.raw_msg = self.consumer.consume(self.queue_name)

        # if no message from queue, perhaps we have message to retry

        if self.raw_msg == None : self.raw_msg = self.retry_get()

        # check if retry message expiry

        if self.raw_msg != None and self.raw_msg.isRetry:
           notice   = self.raw_msg.body
           if type(notice) == bytes: notice = notice.decode("utf-8")
           nparts   = notice.split()
           tparts   = nparts[0].split('.')
           ts       = time.strptime(tparts[0], "%Y%m%d%H%M%S" )
           ep_msg   = calendar.timegm(ts)
           msg_time = ep_msg + int(tparts[1]) / 1000.0

           msg_age  = time.time() - msg_time
           if msg_age > self.parent.retry_ttl :
              self.logger.info("expired retry message skipped %s" % notice)
              self.msg_worked()
              return False, self.msg
           self.logger.info("message is %d seconds old, retry_ttl is %d" % (msg_age, self.parent.retry_ttl ) )


        # when no message sleep for 1 sec. (value taken from old metpx)
        # *** value 0.01 was tested and would simply raise cpu usage of broker
        # to unacceptable level with very fews processes (~20) trying to consume messages
        # remember that instances and broker sharing messages add up to a lot of consumers

        if self.raw_msg == None :
           time.sleep(self.sleep_now)
           self.sleep_now = self.sleep_now * 2
           if self.sleep_now > self.sleep_max : 
                  self.sleep_now = self.sleep_max
           return False, self.msg

        # we have a message, reset timer  (original or retry)

        self.sleep_now = self.sleep_min 

        # make use it as a sr_message
        # dont bother with retry... were good to be kept

        try :
                 self.msg.from_amqplib(self.raw_msg)
                 self.logger.debug("notice %s " % self.msg.notice)
                 if self.msg.urlstr:
                    self.logger.debug("urlstr %s " % self.msg.urlstr)
        except :
                 (stype, svalue, tb) = sys.exc_info()
                 self.logger.error("sr_consumer/consume Type: %s, Value: %s,  ..." % (stype, svalue))
                 self.logger.error("malformed message %s"% vars(self.raw_msg))
                 return None, None

        # special case : pulse

        if self.msg.isPulse :
           self.parent.pulse_count += 1
           return True,self.msg

        # normal message

        if not self.raw_msg.isRetry : self.parent.message_count += 1

        # make use of accept/reject
        # dont bother with retry... were good to be kept
        if self.use_pattern :

           # Adjust url to account for sundew extension if present, and files do not already include the names.
           if urllib.parse.urlparse(self.msg.urlstr).path.count(":") < 1 and 'sundew_extension' in self.msg.headers.keys() :
              urlstr=self.msg.urlstr + ':' + self.msg.headers[ 'sundew_extension' ]
           else:
              urlstr=self.msg.urlstr

           self.logger.debug("sr_consumer, path being matched: %s " % ( urlstr )  ) 

           if not self.parent.isMatchingPattern(self.msg.urlstr,self.accept_unmatch) :
              self.logger.debug("Rejected by accept/reject options")
              return False,self.msg

        elif not self.accept_unmatch :
              return False,self.msg

        # note that it is a retry or not in sr_message

        return True,self.msg

    def get_message(self):
        self.logger.debug("sr_consumer get_message")

        if not hasattr(self.parent,'msg'):
           self.parent.msg = sr_message(self.parent)

        self.raw_msg  = None
        self.msg      = self.parent.msg
        self.msg.user = self.broker.username

    def isAlive(self):
        if not hasattr(self,'consumer') : return False
        if self.consumer.channel == None: return False
        alarm_set(self.iotime)
        try   : self.consumer.channel.basic_qos(0,self.consumer.prefetch,False)
        except: 
                alarm_cancel()
                return False
        alarm_cancel()
        return True

    def msg_to_retry(self):

        if self.raw_msg == None : return

        if self.raw_msg.isRetry : return
        self.logger.info("added to the retry list")

        if self.retry_getmode :
           self.retry_getmode = False
           self.retry_rewrite()

        self.retry_addmode = True
        
        if not os.path.isfile(self.parent.retry_path) :
           self.retry_fp = None
           fp = open(self.parent.retry_path,'w')
           fp.close()

        if self.retry_fp == None :
           self.retry_fp  = open(self.parent.retry_path,'r+')

        topic   = self.raw_msg.delivery_info['routing_key']
        headers = self.raw_msg.properties['application_headers']
        notice  = self.raw_msg.body

        if type(notice) == bytes: notice = notice.decode("utf-8")

        json_line = json.dumps( [ topic, headers, notice ], sort_keys=True ) + '\n' 

        self.retry_fp.seek(0,2)
        self.retry_fp.write( json_line )
        self.retry_fp.flush()
        os.fsync(self.retry_fp)
        self.logger.info("confirmed added to the retry list %s" % notice)

    def msg_worked(self):
        if not self.raw_msg.isRetry : return
        # comment this message not to reprocess again
        self.retry_fp.seek(self.retry_bol,0)
        self.retry_fp.write('//')
        self.retry_fp.seek(self.retry_eol,0)
        self.retry_fp.flush()
        os.fsync(self.retry_fp)

    def publish_back(self):
        self.logger.debug("sr_consumer publish_back")

        self.publisher = Publisher(self.hc)
        self.publisher.build()

        return self.publisher

    def queue_declare(self,build=False):
        self.logger.debug("sr_consumer queue_declare")

        self.durable     = self.parent.durable
        self.reset       = self.parent.reset
        self.expire      = self.parent.expire
        self.message_ttl = self.parent.message_ttl

        # queue name 
        self.set_queue_name()

        # queue settings
        self.msg_queue   = Queue(self.hc,self.queue_name,durable=self.durable,reset=self.reset)

        if self.expire != None :
           self.msg_queue.add_expire(self.expire)

        if self.message_ttl != None :
           self.msg_queue.add_message_ttl(self.message_ttl)

        # queue creation if needed
        if build :
           self.logger.info("declaring queue %s on %s" % (self.queue_name,self.broker.hostname))
           self.msg_queue.build()

    def random_queue_name(self) :

        # queue file : fix it 

        queuefile  = self.parent.program_name
        if self.parent.config_name :
           queuefile += '.' + self.parent.config_name
        queuefile += '.' + self.broker.username

        # queue path

        self.queuepath = self.parent.user_cache_dir + os.sep + queuefile + '.qname'

        # ====================================================
        # FIXME get rid of this code in 2018 (after release 2.17.11a1)
        # transition old queuepath to new queuepath...

        self.old_queuepath = self.parent.user_cache_dir + os.sep + queuefile
        if os.path.isfile(self.old_queuepath) and not os.path.isfile(self.queuepath) :
           # hardlink (copy of old)
           os.link(self.old_queuepath,self.queuepath)
           # during the transition both should be available is we go back

        # get rid up to the next line
        # ====================================================

        if os.path.isfile(self.queuepath) :
           f = open(self.queuepath)
           self.queue_name = f.read()
           f.close()
           return
        
        self.queue_name  = self.queue_prefix 
        self.queue_name += '.'  + self.parent.program_name

        if self.parent.config_name : self.queue_name += '.'  + self.parent.config_name
        if self.parent.queue_suffix: self.queue_name += '.'  + self.parent.queue_suffix

        self.queue_name += '.'  + str(random.randint(0,100000000)).zfill(8)
        self.queue_name += '.'  + str(random.randint(0,100000000)).zfill(8)

        f = open(self.queuepath,'w')
        f.write(self.queue_name)
        f.close()

    def retry_close(self):
        if self.retry_fp == None : return
        try:    
                self.retry_fp.flush()
                os.fsync(self.retry_fp)
                self.retry_fp.close()
        except: pass
        self.retry_fp = None

    def retry_get(self):

        if self.retry_addmode :
           self.retry_close()
           self.retry_addmode = False

        self.retry_getmode = True

        # open (might already be open)

        self.retry_fp  = self.retry_open_rw()
        if self.retry_fp == None : return None

        # get next json_line

        self.retry_bol = self.retry_fp.tell()
        json_line = self.retry_fp.readline()
        if not json_line : 
            self.retry_rewrite()
            return self.retry_get()
        self.retry_eol = self.retry_fp.tell()

        try:
            topic, headers, notice = json.loads(json_line)
        except:
            self.logger.info("corrupted line in retry file: %s " % (json_line))
            self.retry_fp.seek(self.retry_bol,0)
            self.retry_fp.write('//')
            self.retry_fp.seek(self.retry_eol,0)
            self.retry_fp.flush()
            os.fsync(self.retry_fp)
            return None

        self.retry_msg.delivery_info['exchange']         = self.parent.exchange
        self.retry_msg.delivery_info['routing_key']      = topic
        self.retry_msg.properties['application_headers'] = headers
        self.retry_msg.body                              = notice
        self.retry_msg.isRetry = True

        self.retry_getmode = True

        return self.retry_msg

    def retry_open_rw(self):

        if not os.path.isfile(self.parent.retry_path) : return None

        if self.retry_fp != None : return self.retry_fp

        try   : fp = open(self.parent.retry_path,'r+')
        except: return None

        return fp

    def retry_rewrite(self):
        self.logger.debug("retry_rewrite begin")
        
        if not os.path.isfile(self.parent.retry_path) : return

        if self.retry_fp == None :
           try   : self.retry_fp = open(self.parent.retry_path,'r+')
           except: return

        try   : self.retry_fp.seek(0,0)
        except: return

        tmp_path = self.parent.retry_path + '.tmp'
        try:    os.unlink(tmp_path)
        except: pass

        count = 0
        fp    = open(tmp_path,'w')
        while True :
              try:    json_line = self.retry_fp.readline()
              except: json_line = None
              if not json_line             : break
              if json_line.startswith('//'): continue
              fp.write(json_line)
              count += 1
        fp.close()

        self.retry_fp.close()
        self.retry_fp = None
        try:    os.unlink(self.parent.retry_path)
        except: pass

        if count == 0 :
           try:    os.unlink(tmp_path)
           except: pass
           return

        os.rename(tmp_path,self.parent.retry_path)

        if hasattr(self, 'last_retry_rewrite') and ( (time.time() - self.last_retry_rewrite) < 1) :
           if ( self.rewrite_slowdown < 5 ):
               self.rewrite_slowdown*=2;

           self.logger.info("retry_rewrite rewrote %d entries, napping %g second" % (count, self.rewrite_slowdown) )
           time.sleep(self.rewrite_slowdown)
        else:
           self.rewrite_slowdown = 0.01
           self.logger.info("retry_rewrite rewrote %d retries" % count)

        self.last_retry_rewrite=time.time()

    def set_queue_name(self):

        self.broker       = self.parent.broker
        self.queue_prefix = 'q_'+ self.broker.username
        self.queue_name   = self.parent.queue_name

        if self.queue_name :
           if self.queue_prefix in self.queue_name : return
           self.logger.warning("non standard queue name %s" % self.queue_name )
           #self.queue_name = self.queue_prefix + '.'+ self.queue_name
           return

        self.random_queue_name()

    def cleanup(self):
        self.logger.debug("sr_consume cleanup")
        self.build_connection()
        self.set_queue_name()
        self.hc.queue_delete(self.queue_name)
        try    :
                 if hasattr(self,'queuepath') :
                    os.unlink(self.queuepath)
        except : pass

    def declare(self):
        self.logger.debug("sr_consume declare")
        self.build_connection()
        self.queue_declare(build=True)
                  
    def setup(self):
        self.logger.debug("sr_consume setup")
        self.build_connection()
        self.build_queue()


# ===================================
# self_test
# ===================================

class test_logger:
      def silence(self,str):
          pass
      def __init__(self):
          self.debug   = self.silence
          self.error   = print
          self.info    = print
          self.warning = print

def self_test():

    logger = test_logger()

    opt1   = 'accept .*bulletins.*'
    opt2   = 'reject .*'

    #setup consumer to catch first post
    cfg = sr_config()
    cfg.defaults()
    cfg.logger         = logger
    cfg.debug          = True
    #cfg.broker         = urllib.parse.urlparse("amqp://anonymous:anonymous@ddi.cmc.ec.gc.ca/")
    cfg.broker         = urllib.parse.urlparse("amqp://anonymous:anonymous@dd.weather.gc.ca/")
    cfg.prefetch       = 10
    cfg.bindings       = [ ( 'xpublic', 'v02.post.#') ]
    cfg.durable        = False
    cfg.expire         = 60 * 1000 # 60 secs
    cfg.message_ttl    = 10 * 1000 # 10 secs
    cfg.user_cache_dir = os.getcwd()
    cfg.config_name    = "test"
    cfg.queue_name     = None
    cfg.retry_path     = '/tmp/retry'
    cfg.option( opt1.split()  )
    cfg.option( opt2.split()  )

    consumer = sr_consumer(cfg)

    #FIXME setup another consumer
    # from message... log ...  catch log messsage

    i = 0
    while True :
          ok, msg = consumer.consume()
          if ok: break

          i = i + 1
          if i == 100 : 
             msg = None
             break

    os.unlink(consumer.queuepath)

    consumer.close()

    if msg != None :
       if 'bulletins' in msg.notice :
           print("sr_consumer TEST PASSED")
           sys.exit(0)
       print("sr_consumer TEST Failed 1 wrong message")
       sys.exit(1)

    print("sr_consumer TEST Failed 2 no message")
    sys.exit(2)

# ===================================
# MAIN
# ===================================

def main():

    self_test()
    sys.exit(0)

# =========================================
# direct invocation : self testing
# =========================================

if __name__=="__main__":
   main()
