'''
Created on Jan 3, 2018

@author: Salim
'''
from io import  UnsupportedOperation, SEEK_SET, RawIOBase



DEFAULT_CHUNK_SIZE = 2**14


class HttpBufferedOutstream(RawIOBase):
    
    
    
    def __init__(self, conn, chunksize = DEFAULT_CHUNK_SIZE):
        self.conn = conn
        self.__chunksize = chunksize
        self.__buffer = [''] * chunksize
        self.__bufferidx = 0
        self.__closed = False
    
    def writable(self):
        return not self.closed
    
    
    def writelines(self, lines):
        '''
            Write a list of lines to the stream. Line separators are not added, so it is usual for each of the lines provided to have a line separator at the end.
        :param lines:
        '''
        if self.__closed:
            raise OSError()
        for line in lines:
            self.write(line)
            
            
    
    def write(self, b):
        # checking if it is still open
        if self.__closed:
            raise OSError("Conn is already closed")

        # get remaining size of buffer
        remaining = self.__chunksize - self.__bufferidx
        # length of input
        inlen = len(b)
        
        if inlen <=0:
            return 
        
        # if inlen is smaller that remaining size in buffer
        if inlen <= remaining:
            self.__save(b)
            b = []
        else: # if larger, then save then update b to call write again
            self.__save(buffer(b,0,remaining))
            b = buffer(b,remaining, inlen-remaining)
        
        # buffer is full and ready to be written
        if self.__isbufferfull():
            self.flush()
            
        # still something remained in buffer
        if len(b) > 0:
            self.write(b) # call write again for the rest
        
        # it always handles all
        return inlen
            
        
    
    def __isbufferfull(self):
        '''
            Determines if buffer is full and ready to be send to socket
            :return boolean
        '''
        return self.__bufferidx == self.chunksize
    
    def __save(self, b):
        '''
            saves the given data to the buffer
        :param b:
        '''
        newbufferidx = (self.__bufferidx + len(b))
        self.__buffer[self.__bufferidx:newbufferidx] = b
        #update buffer index
        self.__bufferidx = newbufferidx

    
    def flush(self):
        '''
        Flushes the buffer to socket. Only call when the write is done. Calling flush after each write will prevent the buffer to act as efficiently as possible
        '''
        # return if empty
        if self.__bufferidx == 0:
            return 
        # send here the data
        self.conn.send("%s\r\n" % hex(self.__bufferidx)[2:])
        self.conn.send("%s\r\n" % ''.join(self.__buffer[0:self.__bufferidx]))
        # reset buffer index = 0 (beginning of the buffer)
        self.__bufferidx = 0

     
    def close(self):
        '''
        Closes the stream to output. It destroys the buffer and the buffer pointer. However, it will not close the the client connection
        '''
        #write all that is remained in buffer
        self.flush()
        # delete buffer
        self.__buffer = None
        #reset buffer index to -1 to indicate no where
        self.__bufferidx = -1
        #writing the final empty chunk to the socket
        # send here the data
        self.conn.send("0\r\n")
        self.conn.send("\r\n" )
        #set closed flag
        self.__closed = True
        
    
    
    def truncate(self, size= None):
        raise UnsupportedOperation
    
    def tell(self):
        raise UnsupportedOperation
    
    def seekable(self):
        return False
    
    def seek(self, offset, whence = SEEK_SET):
        raise OSError

    def readline(self, size=-1):
        raise OSError

    def readable(self):
        return False

    def readlines(self, hint=-1):
        raise OSError

    def read(self, size  = -1):
        raise OSError

    def readall(self):
        raise OSError
    
    def readinto(self, b):
        raise OSError
    
    def isatty(self):
        return False

    def fileno(self):
        raise OSError()
    
    def __isclosed(self):
        return self.__closed
     
    def __get_chunksize(self):
        return self.__chunksize
    
    def __get_bufferidx(self):
        return self.__bufferidx;

    closed = property(__isclosed)    
    chunksize = property(__get_chunksize)
    buffer_idx = property(__get_bufferidx)
    

