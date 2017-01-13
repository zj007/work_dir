#!/usr/bin/env python
"""
store work path, and chang to it fast.
"""

import sys
import shelve

class Conf(object):
    def __init__(self, conf_file):
        self._file = conf_file
        self._load()

    def _load(self):
        db = shelve.open(self._file)
        try:
            self._conf =db["wd"]
        except:
            self._conf = {}
        db.close()

    def _dump(self):
        db = shelve.open(self._file)
        db["wd"] = self._conf
        db.close()

    def get(self):
        return self._conf
    
    def set(self, new_conf):
        self._conf = new_conf
        self._dump()

class WorkDir(object):
    def __init__(self, conf):
        self._conf = conf
        self._workdirs = conf.get()
        self._cur_wd_mark = '__cur_wd__'

    #add dir
    def add(self, dir_name, mark):
        if mark == self._cur_wd_mark:
            print '%s is reserved mark'%self._cur_wd_mark
            return
        import os.path
        if not os.path.isdir(dir_name):
            print dir_name,' is not a dir'
            return
        self._workdirs[mark] = dir_name
        self._save()
        
    #rm dir
    def remove(self, mark):
        if mark == self._workdirs[self._cur_wd_mark]:
            self._delete_cur_mark()
        del self._workdirs[mark]
        self._save()
    
    def clear(self):
        self._workdirs = {}
        self._save()

    #print dirs
    def p(self):
        #print
        for i,d in self._workdirs.items():
            if i == self._cur_wd_mark:
                continue
            print '[',i,']',' ',d
        #print

    def _update_cur_mark(self, mark):
        self._workdirs[self._cur_wd_mark] = mark
        self._save()

    def _delete_cur_mark(self):
        del self._workdirs[self._cur_wd_mark]

    def _save(self):
        self._conf.set(self._workdirs)
    
    #change to the top  work dir
    def jump(self, mark):
        if self._workdirs:
            sh_f = open("~/bin/go",'w') #go to store the dir you want to cd
            ctx=['#!/bin/sh','cd '+self._workdirs[mark]]
            sh_f.writelines([l+'\n' for l in ctx])
            sh_f.close()
            self._update_cur_mark(mark)

    def get_cur_wd(self):
        if self._cur_wd_mark in self._workdirs:
            m = self._workdirs[self._cur_wd_mark]
            if m in self._workdirs:
                return self._workdirs[m]
        return 'none'
        
    def help(self):
        print   '. go --jump to the specified dir in workdirs\n'\
                '\twd -add dir [m]mark : add dir to workdirs with mark\n'\
                '\twd -l               : list dirs in workdirs\n'\
                '\twd -rm m[mark]      : delete dir whose mark is m in workdirs\n'\
                '\twd -h               : help of workdir\n'\
                '\twd -i m[mark]       : let the dir whose mark is m be the specified dir\n'\
                '\twd -p m[mark]       : add dir via pipe\n'\
                '\twd -c               : clear all marks'


def main():
    _conf_file = '~/bin/.label_dir_store'
    _work = WorkDir(Conf(_conf_file))
    argv = sys.argv
    
    if len(argv) == 1:
        print "version 1.0"
        print 'current work path : %s'%(_work.get_cur_wd())
        return
    if argv[1] in ['-add'] and len(argv) != 4:
        print "wd -d need more arguments"
        _work.help()
        return

    if argv[1] in ['-rm','-i', '-p'] and len(argv) !=3:
        print '[ -d -rm -i ] should have argument'
        _work.help()
        return
    
    cmd = argv[1]

    if cmd == '-p':
        _work.add(list(sys.stdin)[0].strip(), argv[2])
    elif cmd == '-add':
        _work.add(argv[2], argv[3])
    elif cmd == '-l':
        _work.p()
    elif cmd == '-rm':
        _work.remove(argv[2])
    elif cmd == '-h':
        _work.help()
    elif cmd == '-i':
        _work.jump(argv[2])
    elif cmd == '-c':
        _work.clear()
    else:
        print 'the cmd is not recognized'
        _work.help()

if __name__ == '__main__':
    main()
