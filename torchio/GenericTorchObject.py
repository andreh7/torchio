#!/usr/bin/env python
class GenericTorchObject:

    def __str__(self):
        retval = self.__class__.__name__ + " {"
        
        for key, value in self.__dict__.items():
            retval += ' ' + str(key) + "=" + str(value)

        retval += " }"

        return retval

