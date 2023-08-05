import sys
import umsgpack

class UmsgpackClassCoder:
    """
    Abstract class encoder and decoder.
    Allow encode and decode classes.
    """

    def encode(self, obj):
        """ Override to encode object. """
        raise NotImplementedError()

    def decode(self, data):
        """ Override to decode object. """
        raise NotImplementedError()


class UmsgpackClassDefaultCoder(UmsgpackClassCoder):
    """
    Class basic encoder and decoder.
    Allow encode almost all classes without custom coding.
    It uses __dict__, __slots__ with mro to learn attributes.
    """

    @classmethod
    def encode(cls, obj):
        """ Encode class attributes. """
        encoded = {}

        # encode __dict__ attributes
        if hasattr(obj, '__dict__'):
            for attr, value in obj.__dict__.items():
                encoded[attr] = value

        # encode __slots__ attributes
        for cls in obj.__class__.__mro__:
            if hasattr(cls, '__slots__'):
                # __slots__ can be string
                if isinstance(cls.__slots__, str):
                    attr = cls.__slots__
                    if hasattr(obj, attr):
                        encoded[attr] = getattr(obj, attr)
                # __slots__ can be iterable
                else:
                    for attr in cls.__slots__:
                        if hasattr(obj, attr):
                            encoded[attr] = getattr(obj, attr)
        return encoded

    @classmethod
    def decode(cls, obj, encoded):
        """ Decode attributes. """
        for attr, value in encoded.items():
            setattr(obj, attr, value)
        return obj


class UmsgpackCoder:
    """
    Simple interface to umsgpack.
    """

    def __init__(self):
        self.classes_coders = {}
        """ umsgpack custom classes coders. """

    def set_default_coder_for_class(self, cls):
        """
        Set default coder for class.
        For security you need register all classes.
        """
        self.classes_coders[cls] = UmsgpackClassDefaultCoder

    # metadata identifiers
    MODULE_NAME = 0
    CLASS_NAME = 1
    CLASS_DATA = 2

    def _ext_encoder(self, obj, obj_encoded, ext_handlers):
        """ Classes metadata default encoder. """
        encoded = {}

        # encode module and class name if no id
        encoded[self.MODULE_NAME] = obj.__class__.__module__
        encoded[self.CLASS_NAME] = obj.__class__.__qualname__
        encoded[self.CLASS_DATA] = obj_encoded

        return umsgpack.Ext(0, umsgpack.packb(encoded, ext_handlers=ext_handlers))

    def _ext_dump(self):
        """ Get list of encoders. """
        ext_encoders = {}
        for cls, coder in self.classes_coders.items():
            ext_encoders[cls] = lambda o: self._ext_encoder(o, coder.encode(o), self._ext_dump())
        return ext_encoders

    def _ext_object_decode(self, encoded):
        module_name = encoded[self.MODULE_NAME]
        class_name = encoded[self.CLASS_NAME]

        # get module if loaded
        module = sys.modules.get(module_name)
        # load module if not loaded
        if module is None:
            __import__(module_name)
            module = sys.modules[module_name]

        # get class from module
        cls = getattr(module, class_name)

        # get coder for class
        coder = self.classes_coders[cls]

        return coder.decode(encoded[self.CLASS_DATA])

    def _ext_decode(self, ext):
        """ True decoder which read class name. """
        decoded = umsgpack.unpackb(ext.data, ext_handlers=self._ext_load())
        module_name = decoded[self.MODULE_NAME]
        class_name = decoded[self.CLASS_NAME]

        # get module if loaded
        module = sys.modules.get(module_name)
        # load module if not loaded
        if module is None:
            __import__(module_name)
            module = sys.modules[module_name]

        # class can be nested
        name_parts = class_name.split('.')

        cls = module
        for name_part in name_parts:
            cls = getattr(cls, name_part)

        # create object
        obj = object.__new__(cls)

        coder = self.classes_coders[cls]

        coder.decode(obj, decoded[self.CLASS_DATA])

        return obj

    def _ext_load(self):
        """ Get list of decoders. """
        return {0: self._ext_decode}

    def dump(self, obj, f):
        """ Dump object to file stream. """
        umsgpack.pack(obj, f, ext_handlers=self._ext_dump())

    def dumps(self, obj):
        """ Dump object to bytes array. """
        return umsgpack.packb(obj, ext_handlers=self._ext_dump())

    def load(self, f):
        """ Load object from file stream. """
        return umsgpack.unpack(f, ext_handlers=self._ext_load())

    def loads(self, b):
        """ Load object from bytes array. """
        return umsgpack.unpackb(b, ext_handlers=self._ext_load())
