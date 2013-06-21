# -*- mode: python; coding: utf-8 -*-
#
# Copyright 2013 Andrej A Antonov <polymorphm@gmail.com>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

assert str is not bytes

import socket, time, random

CONNECT_PORT = 80
CONNECT_TIMEOUT = 300.0

class StatusCtx:
    pass

def create_agent(agent_name, addr_info_list):
    while True:
        sock = None
        
        try:
            if not addr_info_list:
                raise OSError
            
            addr_info = random.choice(addr_info_list)
            sock = socket.socket(addr_info[0], addr_info[1], addr_info[2])
            
            sock.setblocking(False)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            
            is_connected = False
            begin_con_time = time.time()
            
            try:
                sock.connect(addr_info[3], addr_info[4])
            except BlockingIOError:
                pass
            else:
                is_connected = True
            
            yield 'new_con'
            
            while not is_connected:
                try:
                    sock.connect(addr_info[3], addr_info[4]):
                except BlockingIOError:
                    pass
                else:
                    is_connected = True
                    break
                
                curr_time = time.time()
                
                if curr_time < begin_con_time:
                    begin_con_time = curr_time
                
                if curr_time > begin_con_time + CONNECT_TIMEOUT:
                    sock.close()
                    raise OSError
                
                yield 'contin_con'
            
            while True:
                # TODO ... делаем дело
                
                # TODO если ошибка то ---- raise OSError
                
                yield 'work'
        except OSError:
            if sock is not None:
                sock.close()
                sock = None
            
            yield 'error'

def print_status(status_ctx):
    text = \
            '# {dt}\n' \
            '{new_cons_label:<24}{new_cons:>8}\n' \
            '{contin_cons_label:<24}{contin_cons:>8}\n' \
            '{works_label:<24}{works:>8}\n' \
            '{errors_label:<24}{errors:>8}'.format(
                    dt=time.ctime(),
                    new_cons_label='new connects:',
                    new_cons=status_ctx.new_cons,
                    contin_cons_label='continue connects:',
                    contin_cons=status_ctx.contin_cons,
                    works_label='in working:',
                    works=status_ctx.works,
                    errors_label='errors:',
                    errors=status_ctx.errors,
                    )
    
    print(text)

def con_array_test(hostname, con_count, delay):
    addr_info_list = socket.getaddrinfo(
            hostname,
            CONNECT_PORT,
            proto=socket.SOL_TCP,
            )
    
    agent_list = tuple(
            create_agent('agent_{}'.format(con_i), addr_info_list)
            for con_i in range(con_count)
            )
    
    print('Agent list initialized')
    
    while True:
        status_ctx = StatusCtx()
        
        status_ctx.new_cons = 0
        status_ctx.contin_cons = 0
        status_ctx.works = 0
        status_ctx.errors = 0
        
        for agent in agent_list:
            agent_status = next(agent)
            
            if agent_status == 'new_con':
                status_ctx.new_cons += 1
            elif agent_status == 'contin_con':
                status_ctx.contin_cons += 1
            elif agent_status == 'work':
                status_ctx.works += 1
            elif agent_status == 'error':
                status_ctx.errors += 1
            else:
                raise NotImplementedError
            
            time.sleep(delay)
        
        print_status(status_ctx)
