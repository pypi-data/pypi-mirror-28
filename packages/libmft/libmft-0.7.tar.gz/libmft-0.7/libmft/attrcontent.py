# -*- coding: utf-8 -*-
'''
This module contains all the known information about attributes. In particular,
their content. By definition, as we have only the $MFT available for processing
we can't have any of the content in case of non-resident attributes.
That means that all the classes below EXPECT the attribute to be resident.

Calling the constructors for a non-resident attribute MAY lead to an unxpected
behaviour.
'''
import struct
import logging
from itertools import chain as _chain
from operator import getitem as _getitem

from libmft.util.functions import convert_filetime, get_file_reference
from libmft.flagsandtypes import AttrTypes, NameType, FileInfoFlags, \
    IndexEntryFlags, VolumeFlags, ReparseType, ReparseFlags, CollationRule

_MOD_LOGGER = logging.getLogger(__name__)

#TODO verify, in general, if it is not better to encode the data within the
#attributes as tuple or list and use properties to access by name

#TODO rewrite the commentaries

#******************************************************************************
# STANDARD_INFORMATION ATTRIBUTE
#******************************************************************************
class StandardInformation():
    '''Represents the STANDARD_INFORMATION converting the timestamps to
    datetimes and the flags to FileInfoFlags representation.'''
    #_REPR = struct.Struct("<4Q4I")
    _REPR = struct.Struct("<4QI12x")
    _REPR_NFTS_3_EXTENSION = struct.Struct("<2I2Q")
    ''' Creation time - 8
        File altered time - 8
        MFT/Metadata altered time - 8
        Accessed time - 8
        Flags - 4 (FileInfoFlags)
        Maximum number of versions - 4
        Version number - 4
        Class id - 4
        Owner id - 4 (NTFS 3+)
        Security id - 4 (NTFS 3+)
        Quota charged - 8 (NTFS 3+)
        Update Sequence Number (USN) - 8 (NTFS 3+)
    '''

    def __init__(self, content=(None,)*9):
        '''Creates a StandardInformation object. The content has to be an iterable
        with precisely 0 elements in order.
        If content is not provided, a 0 element tuple, where all elements are
        None, is the default argument

        Args:
            content (iterable), where:
                [0] (datetime) - created time
                [1] (datetime) - changed time
                [2] (datetime) - mft change time
                [3] (datetime) - accessed
                [4] (FileInfoFlags) - flags
                [5] (int) - Owner id
                [6] (int) - Security id
                [7] (int) - Quota charged
                [8] (int) - Update Sequence Number
        '''
        self.timestamps = {}

        self.timestamps["created"], self.timestamps["changed"], \
        self.timestamps["mft_change"], self.timestamps["accessed"], \
        self.flags, self.owner_id, \
        self.security_id, self.quota_charged, self.usn = content

    @classmethod
    def get_static_content_size(cls):
        '''Returns the static size of the content never taking in consideration
        variable fields, for example, names.

        Returns:
            int: The size of the content, in bytes
        '''
        return cls._REPR.size + cls._REPR_NFTS_3_EXTENSION.size

    @classmethod
    def create_from_binary(cls, binary_view):
        '''Creates a new object StandardInformation from a binary stream. The binary
        stream can be represented by a byte string, bytearray or a memoryview of the
        bytearray.

        Args:
            binary_view (memoryview of bytearray) - A binary stream with the
                information of the attribute

        Returns:
            StandardInformation: New object using hte binary stream as source
        '''
        _MOD_LOGGER.debug("Unpacking STANDARD_INFORMATION content")
        main_content = cls._REPR.unpack(binary_view[:cls._REPR.size])
        if len(binary_view) != cls._REPR.size:
            _MOD_LOGGER.debug("Unpacking NTFS 3 extesion")
            ntfs3_extension = cls._REPR_NFTS_3_EXTENSION.unpack(binary_view[cls._REPR.size:])
        else:
            ntfs3_extension = (None, None, None, None)
        #create the new object with "raw types"
        nw_obj = cls(_chain(main_content, ntfs3_extension))
        #update the object converting to the correct types
        nw_obj.timestamps["created"] = convert_filetime(nw_obj.timestamps["created"])
        nw_obj.timestamps["changed"] = convert_filetime(nw_obj.timestamps["changed"])
        nw_obj.timestamps["mft_change"] = convert_filetime(nw_obj.timestamps["mft_change"])
        nw_obj.timestamps["accessed"] = convert_filetime(nw_obj.timestamps["accessed"])
        nw_obj.flags = FileInfoFlags(nw_obj.flags)
        _MOD_LOGGER.debug("StandardInformation object created successfully")

        return nw_obj

    def get_created_time(self):
        '''Returns the created time. This function provides the same information
        as using <variable>.timestamps["created"].

        Returns:
            datetime: The created time'''
        return self.timestamps["created"]

    def get_changed_time(self):
        '''Returns the changed time. This function provides the same information
        as using <variable>.timestamps["changed"].

        Returns:
            datetime: The changed time'''
        return self.timestamps["changed"]

    def get_mftchange_time(self):
        '''Returns the mft change time. This function provides the same information
        as using <variable>.timestamps["mft_change"].

        Returns:
            datetime: The mft change time'''
        return self.timestamps["mft_change"]

    def get_accessed_time(self):
        '''Returns the accessed time. This function provides the same information
        as using <variable>.timestamps["accessed"].

        Returns:
            datetime: The accessed time'''
        return self.timestamps["accessed"]

    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + '(timestamps={}, flags={!s}, owner_id={}, security_id={}, quota_charged={}, usn={})'.format(
            self.timestamps, self.flags, self.owner_id, self.security_id,
            self.quota_charged, self.usn)

#******************************************************************************
# ATTRIBUTE_LIST ATTRIBUTE
#******************************************************************************
class AttributeListEntry():
    '''This class holds one entry on the attribute list attribute.'''
    _REPR = struct.Struct("<IH2B2QH")
    '''
        Attribute type - 4
        Length of a particular entry - 2
        Length of the name - 1 (in characters)
        Offset to name - 1
        Starting VCN - 8
        File reference - 8
        Attribute ID - 1
        Name (unicode) - variable
    '''

    def __init__(self, content=(None,)*9):
        '''Creates an AttributeListEntry object. The content has to be an iterable
        with precisely 9 elements in order.
        If content is not provided, a tuple filled with 'None' is the default
        argument.

        Args:
            content (iterable), where:
                [0] (AttrTypes) - Attribute type
                [1] (int) - length of the entry
                [2] (int) - length of the name
                [3] (int) - offset to the name
                [4] (int) - start vcn
                [5] (int) - file reference number
                [6] (int) - file sequence number
                [7] (int) - attribute id
                [8] (str) - name
        '''
        self.attr_type, self.entry_len, _, self.name_offset, \
        self.start_vcn, self.file_ref, self.file_seq, self.attr_id, self.name = content

    def _get_name_length(self):
        '''Returns the length of the name based on the name'''
        if self.name is None:
            return 0
        else:
            return len(self.name)

    @classmethod
    def get_static_content_size(cls):
        '''Returns the static size of the content never taking in consideration
        variable fields, for example, names.

        Returns:
            int: The size of the content, in bytes
        '''
        return cls._REPR.size

    @classmethod
    def create_from_binary(cls, binary_view):
        '''Creates a new object AttributeListEntry from a binary stream. The binary
        stream can be represented by a byte string, bytearray or a memoryview of the
        bytearray.

        Args:
            binary_view (memoryview of bytearray) - A binary stream with the
                information of the attribute

        Returns:
            AttributeListEntry: New object using hte binary stream as source
        '''
        _MOD_LOGGER.debug("Unpacking ATTRIBUTE_LIST content")
        content = cls._REPR.unpack(binary_view[:cls._REPR.size])
        nw_obj = cls()

        if content[2]:
            name = binary_view[content[3]:content[3]+(2*content[2])].tobytes().decode("utf_16_le")
        else:
            name = None
        file_ref, file_seq = get_file_reference(content[5])
        nw_obj.attr_type, nw_obj.entry_len, nw_obj.name_offset, nw_obj.start_vcn,  \
        nw_obj.file_ref, nw_obj.file_seq, nw_obj.attr_id, nw_obj.name = \
        AttrTypes(content[0]), content[1], content[3], content[4], \
        file_ref, file_seq, content[6], name
        _MOD_LOGGER.debug("AttributeListEntry object created successfully")

        return nw_obj

    #the name length can derived from the name, so, we don't need to keep in memory
    name_len = property(_get_name_length, doc='Length of the name')

    def __len__(self):
        '''Returns the size of the entry, in bytes'''
        return self.entry_len

    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + '(attr_type={!s}, entry_len={}, name_len={}, name_offset={}, start_vcn={}, file_ref={}, file_seq={}, attr_id={}, name={})'.format(
            self.attr_type, self.entry_len, self.name_len, self.name_offset,
            self.start_vcn, self.file_ref, self.file_seq, self.attr_id, self.name)

class AttributeList():
    '''Represents the ATTRIBUTE_LIST attribute, holding all the entries, if available,
    as AttributeListEntry objects.'''

    def __init__(self, content=[]):
        '''Creates an AttributeList content representation. Content has to be a
        list of AttributeListEntry that will be referred by the object. To create
        from a binary string, use the function 'create_from_binary' '''
        self.attr_list = content

    @classmethod
    def create_from_binary(cls, binary_view):
        '''Creates a new object AttributeList from a binary stream. The binary
        stream can be represented by a byte string, bytearray or a memoryview of the
        bytearray. As the AttributeList is a contatiner, the binary stream has
        to have multiple AttributeListEntry encoded.

        Args:
            binary_view (memoryview of bytearray) - A binary stream with the
                information of multiple AttributeListEntry

        Returns:
            AttributeList: New object using the binary stream as source
        '''
        attr_list = []
        offset = 0

        while True:
            _MOD_LOGGER.debug("Creating AttributeListEntry object from binary stream...")
            entry = AttributeListEntry.create_from_binary(binary_view[offset:])
            offset += entry.entry_len
            attr_list.append(entry)
            if offset >= len(binary_view):
                break
            _MOD_LOGGER.debug(f"Next AttributeListEntry offset = {offset}")
        _MOD_LOGGER.debug("AttributeListEntry object created successfully")

        return cls(attr_list)

    def __len__(self):
        '''Return the number of entries in the attribute list'''
        return len(self.attr_list)

    def __iter__(self):
        '''Return the iterator for the representation of the list, so it is
        easier to check everything'''
        return iter(self.attr_list)

    def __getitem__(self, index):
        '''Return the AttributeListEntry at the specified position'''
        return _getitem(self.attr_list, index)

    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + '(attr_list={})'.format(
            self.attr_list)

#******************************************************************************
# OBJECT_ID ATTRIBUTE
#******************************************************************************
class UID():
    '''This class represents an UID as defined by Microsoft and used in the
    MFT entries. Consult https://msdn.microsoft.com/en-us/library/cc227517.aspx
    for information.'''
    _REPR = struct.Struct("<2Q")
    ''' Object ID - 8
        Volume ID - 8
    '''
    def __init__(self, content=(None,)*2):
        '''Creates an UID object. The content has to be an iterable
        with precisely 2 elements in order.
        If content is not provided, a 2 element tuple, where all elements are
        None, is the default argument.

        Args:
            content (iterable), where:
                [0] (int) - object id
                [1] (int) - volume_id
        '''
        self.object_id, self.volume_id = content

    @classmethod
    def get_uid_size(cls):
        '''Returns the static size of the content never taking in consideration
        variable fields, for example, names.

        Returns:
            int: The size of the content, in bytes
        '''
        return cls._REPR.size

    @classmethod
    def create_from_binary(cls, binary_view):
        '''Creates a new object UID from a binary stream. The binary
        stream can be represented by a byte string, bytearray or a memoryview of the
        bytearray.

        Args:
            binary_view (memoryview of bytearray) - A binary stream with the
                information of an UID

        Returns:
            UID: New object using the binary stream as source
        '''
        return cls(cls._REPR.unpack(binary_view[:cls._REPR.size]))

    #TODO comparison methods

    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + '(volume_id={:#010x}, object_id={:#010x})'.format(
            self.volume_id, self.object_id)

class ObjectID():
    '''This class represents an Object ID.'''

    def __init__(self,  content=(None,)*4):
        '''Creates a StandardInformation object. The content has to be an iterable
        with precisely 4 elements in order.
        If content is not provided, a 4 element tuple, where all elements are
        None, is the default argument.

        Args:
            content (iterable), where:
                [0] (UID) - object id
                [1] (UID) - birth volume id
                [2] (UID) - virth object id
                [3] (UID) - birth domain id
        '''
        self.object_id, self.birth_vol_id, self.birth_object_id, \
        self.birth_domain_id = content

    @classmethod
    def create_from_binary(cls, binary_view):
        '''Creates a new object ObjectID from a binary stream. The binary
        stream can be represented by a byte string, bytearray or a memoryview of the
        bytearray.

        Args:
            binary_view (memoryview of bytearray) - A binary stream with the
                information of an ObjectID

        Returns:
            ObjectID: New object using the binary stream as source
        '''
        uid_size = UID.get_uid_size()

        #some entries might not have all four ids, this line forces
        #to always create 4 elements, so contruction is easier
        uids = [UID.create_from_binary(binary_view[i*uid_size:(i+1)*uid_size]) if i * uid_size < len(binary_view) else None for i in range(0,4)]
        _MOD_LOGGER.debug("ObjectID object created successfully")

        return cls(uids)

    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + '(object_id={}, birth_vol_id={}, birth_object_id={}, birth_domain_id={})'.format(
            self.object_id, self.birth_vol_id, self.birth_object_id, self.birth_domain_id)

#******************************************************************************
# VOLUME_NAME ATTRIBUTE
#******************************************************************************
class VolumeName():
    '''This class represents a VolumeName attribute.'''
    def __init__(self, name):
        '''Initialize a VolumeName object, receives the name of the volume:

        Args:
            name (str) - name of the volume
        '''
        self.name = name

    @classmethod
    def create_from_binary(cls, binary_view):
        '''Creates a new object VolumeName from a binary stream. The binary
        stream can be represented by a byte string, bytearray or a memoryview of the
        bytearray.

        Args:
            binary_view (memoryview of bytearray) - A binary stream with the
                information of an VolumeName

        Returns:
            VolumeName: New object using the binary stream as source
        '''
        name = binary_view.tobytes().decode("utf_16_le")
        _MOD_LOGGER.debug("ObjectID object created successfully")

        return cls(name)

    def __len__(self):
        '''Returns the length of the name'''
        return len(self.name)

    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + '(name={})'.format(
            self.name)

#******************************************************************************
# VOLUME_INFORMATION ATTRIBUTE
#******************************************************************************
class VolumeInformation():
    '''This class represents a VolumeInformation attribute.'''

    _REPR = struct.Struct("<Q2BH")
    ''' Unknow - 8
        Major version number - 1
        Minor version number - 1
        Volume flags - 2
    '''

    def __init__(self, content=(None,)*3):
        '''Creates a VolumeInformation object. The content has to be an iterable
        with precisely 3 elements in order.
        If content is not provided, a 3 element tuple, where all elements are
        None, is the default argument

        Args:
            content (iterable), where:
                [0] (int) - major version
                [1] (int) - minor version
                [2] (VolumeFlags) - Volume flags
        '''
        self.major_ver, self.minor_ver, self.vol_flags = content

    @classmethod
    def create_from_binary(cls, binary_view):
        '''Creates a new object VolumeInformation from a binary stream. The binary
        stream can be represented by a byte string, bytearray or a memoryview of the
        bytearray.

        Args:
            binary_view (memoryview of bytearray) - A binary stream with the
                information of an VolumeInformation

        Returns:
            VolumeInformation: New object using the binary stream as source
        '''
        nw_obj = cls()
        content = cls._REPR.unpack(binary_view)

        nw_obj.major_ver, nw_obj.minor_ver, nw_obj.vol_flags = content[1], \
            content[2], VolumeFlags(content[3])
        _MOD_LOGGER.debug("VolumeInformation object created successfully")

        return nw_obj

    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + '(major_ver={}, minor_ver={}, vol_flags={!s})'.format(
            self.major_ver, self.minor_ver, self.vol_flags)

#******************************************************************************
# FILENAME ATTRIBUTE
#******************************************************************************
class FileName():
    '''Represents the FILE_NAME converting the timestamps to
    datetimes and the flags to FileInfoFlags representation.
    '''
    #_REPR = struct.Struct("<7Q2I2B")
    _REPR = struct.Struct("<5Q16x2I2B")
    ''' File reference to parent directory - 8
        Creation time - 8
        File altered time - 8
        MFT/Metadata altered time - 8
        Accessed time - 8
        Allocated size of file - 8 (multiple of the cluster size)
        Real size of file - 8 (actual file size, might also be stored by the directory)
        Flags - 4
        Reparse value - 4
        Name length - 1 (in characters)
        Name type - 1
        Name - variable
    '''
    def __init__(self, content=(None, )*11):
        '''Creates a FileName object. The content has to be an iterable
        with precisely 11 elements in order.
        If content is not provided, a tuple filled with 'None' is the default
        argument.

        Args:
            content (iterable), where:
                [0] (int) - parent refence
                [1] (int) - parent sequence
                [2] (datetime) - created time
                [3] (datetime) - changed time
                [4] (datetime) - mft change time
                [5] (datetime) - accessed
                [7] (FileInfoFlags) - flags
                [8] (int) - reparse value
                [9] (int) - name length
                [10] (NameType) - name type
                [11] (str) - name
        '''
        self.timestamps = {}

        self.parent_ref, self.parent_seq, self.timestamps["created"], \
        self.timestamps["changed"], self.timestamps["mft_change"], \
        self.timestamps["accessed"], \
        self.flags, self.reparse_value, _, self.name_type, \
        self.name = content

    def _get_name_len(self):
        return len(self.name)

    #the name length can derived from the name, so, we don't need to keep in memory
    name_len = property(_get_name_len, doc='Length of the name')

    @classmethod
    def get_static_content_size(cls):
        '''Returns the static size of the content never taking in consideration
        variable fields, for example, names.

        Returns:
            int: The size of the content, in bytes
        '''
        return cls._REPR.size

    @classmethod
    def create_from_binary(cls, binary_view):
        '''Creates a new object FileName from a binary stream. The binary
        stream can be represented by a byte string, bytearray or a memoryview of the
        bytearray.

        Args:
            binary_view (memoryview of bytearray) - A binary stream with the
                information of an FileName

        Returns:
            FileName: New object using the binary stream as source
        '''
        nw_obj = cls()
        content = cls._REPR.unpack(binary_view[:cls._REPR.size])
        name = binary_view[cls._REPR.size:].tobytes().decode("utf_16_le")

        file_ref, file_seq = get_file_reference(content[0])
        nw_obj.parent_ref, nw_obj.parent_seq, nw_obj.timestamps["created"], \
        nw_obj.timestamps["changed"], nw_obj.timestamps["mft_change"], \
        nw_obj.timestamps["accessed"], nw_obj.flags, nw_obj.reparse_value, \
        nw_obj.name_type, nw_obj.name = \
        file_ref, file_seq, convert_filetime(content[1]), \
        convert_filetime(content[2]), convert_filetime(content[3]), \
        convert_filetime(content[4]), FileInfoFlags(content[5]), \
        content[6], NameType(content[8]), name

        return nw_obj

    def get_created_time(self):
        '''Return the created time. This function provides the same information
        as using <variable>.timestamps["created"]'''
        return self.timestamps["created"]

    def get_changed_time(self):
        '''Return the changed time. This function provides the same information
        as using <variable>.timestamps["changed"]'''
        return self.timestamps["changed"]

    def get_mftchange_time(self):
        '''Return the mft change time. This function provides the same information
        as using <variable>.timestamps["mft_change"]'''
        return self.timestamps["mft_change"]

    def get_accessed_time(self):
        '''Return the accessed time. This function provides the same information
        as using <variable>.timestamps["accessed"]'''
        return self.timestamps["accessed"]

    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + '(parent_ref={}, parent_seq={}, timestamps={}, reparse_value={}, flags={!s}, name_len={}, name_type={!s}, name={})'.format(
            self.parent_ref, self.parent_seq, self.timestamps, self.reparse_value,
            self.flags, self.name_len, self.name_type, self.name)

#******************************************************************************
# DATA ATTRIBUTE
#******************************************************************************
class Data():
    '''This is a placeholder class to the data attribute. By itself, it does
    very little and holds almost no information. If the data is resident, holds the
    content and the size.
    '''
    def __init__(self, bin_view):
        '''Initialize the class. Expects the binary_view that represents the
        content. Size information is derived from the content.
        '''
        self.content = bin_view.tobytes()

    def __len__(self):
        '''Returns the logical size of the file'''
        return len(self.content)

    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + '(content={})'.format(
            self.content)

#******************************************************************************
# INDEX_ROOT ATTRIBUTE
#******************************************************************************
class IndexNodeHeader():
    '''Represents the Index Node Header, that is always present in the INDEX_ROOT
    and INDEX_ALLOCATION attribute.'''

    _REPR = struct.Struct("<4I")
    ''' Offset to start of index entry - 4
        Offset to end of used portion of index entry - 4
        Offset to end of the allocated index entry - 4
        Flags - 4
    '''

    def __init__(self, content=(None,)*4):
        '''Creates a IndexNodeHeader object. The content has to be an iterable
        with precisely 4 elements in order.
        If content is not provided, a 4 element tuple, where all elements are
        None, is the default argument

        Args:
            content (iterable), where:
                [0] (int) - start offset
                [1] (int) - end offset
                [2] (int) - allocated size of the node
                [3] (int) - non-leaf node Flag (has subnodes)
        '''
        self.start_offset, self.end_offset, self.end_alloc_offset, \
        self.flags = content

    @classmethod
    def get_static_content_size(cls):
        '''Returns the static size of the content never taking in consideration
        variable fields, for example, names.

        Returns:
            int: The size of the content, in bytes
        '''
        return cls._REPR.size

    @classmethod
    def create_from_binary(cls, binary_view):
        '''Creates a new object IndexNodeHeader from a binary stream. The binary
        stream can be represented by a byte string, bytearray or a memoryview of the
        bytearray.

        Args:
            binary_view (memoryview of bytearray) - A binary stream with the
                information of an IndexNodeHeader

        Returns:
            IndexNodeHeader: New object using the binary stream as source
        '''
        nw_obj = cls(cls._REPR.unpack(binary_view[:cls._REPR.size]))
        _MOD_LOGGER.debug("IndexNodeHeader object created successfully")

        return nw_obj

    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + '(start_offset={}, end_offset={}, end_alloc_offset={}, flags={})'.format(
            self.start_offset, self.end_offset, self.end_alloc_offset, self.flags)

class IndexEntry():
    '''Represents an entry in the index.'''

    _REPR = struct.Struct("<Q2HI")
    ''' Undefined - 8
        Length of entry - 2
        Length of content - 2
        Flags - 4
        Content - variable
        VCN of child node - 8 (exists only if flag is set, aligned to a 8 byte boundary)
    '''
    _REPR_VCN = struct.Struct("<Q")

    def __init__(self, content=(None,)*6):
        '''Creates a StandardInformation object. The content has to be an iterable
        with precisely 0 elements in order.
        If content is not provided, a 0 element tuple, where all elements are
        None, is the default argument

        Args:
            content (iterable), where:
                [0] (int) - file reference?
                [1] (int) - length of the entry
                [2] (int) - length of the content
                [3] (int) - flags (1 = index has a sub-node, 2 = last index entry in the node)
                [4] (FileName or binary_string) - content
                [5] (int) - vcn child node
        '''
        #TODO don't save this here and overload later?
        #TODO confirm if this is really generic or is always a file reference
        #this generic variable changes depending what information is stored
        #in the index
        self.generic, self.entry_len, self.content_len, self.flags, \
        self.content, self.vcn_child_node = content

    @classmethod
    def get_static_content_size(cls):
        '''Returns the static size of the content never taking in consideration
        variable fields, for example, names.

        Returns:
            int: The size of the content, in bytes
        '''
        return cls._REPR.size

    @classmethod
    def create_from_binary(cls, binary_view, content_type=None):
        '''Creates a new object IndexEntry from a binary stream. The binary
        stream can be represented by a byte string, bytearray or a memoryview of the
        bytearray.

        Args:
            binary_view (memoryview of bytearray) - A binary stream with the
                information of an IndexEntry
            content_type (AttrTypes) - Type of content present in the index

        Returns:
            IndexEntry: New object using the binary stream as source
        '''
        repr_size = cls._REPR.size
        content = cls._REPR.unpack(binary_view[:repr_size])
        nw_obj = cls()

        vcn_child_node = (None,)
        #if content is known (filename), create a new object to represent the content
        if content_type is AttrTypes.FILE_NAME and content[2]:
            binary_content = FileName.create_from_binary(binary_view[repr_size:repr_size+content[2]])
        else:
            binary_content = binary_view[repr_size:repr_size+content[2]].tobytes()
        #if there is a next entry, we need to padd it to a 8 byte boundary
        if content[3] & IndexEntryFlags.CHILD_NODE_EXISTS:
            temp_size = repr_size + content[2]
            boundary_fix = (content[1] - temp_size) % 8
            vcn_child_node = cls._REPR_VCN.unpack(binary_view[temp_size+boundary_fix:temp_size+boundary_fix+8])

        nw_obj.generic, nw_obj.entry_len, nw_obj.content_len, nw_obj.flags, \
        nw_obj.content, nw_obj.vcn_child_node = content[0], content[1], content[2], \
            IndexEntryFlags(content[3]), binary_content, vcn_child_node
        _MOD_LOGGER.debug("IndexEntry object created successfully")

        return nw_obj

    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + '(generic={}, entry_len={}, content_len={}, flags={!s}, content={}, vcn_child_node={})'.format(
            self.generic, self.entry_len, self.content_len, self.flags,
            self.content, self.vcn_child_node)

class IndexRoot():
    '''Represents the INDEX_ROOT'''

    _REPR = struct.Struct("<3IB3x")
    ''' Attribute type - 4
        Collation rule - 4
        Bytes per index record - 4
        Clusters per index record - 1
        Padding - 3
    '''

    def __init__(self, content=(None,)*4, node_header=None, idx_entry_list=None):
        '''Creates a IndexRoot object. The content has to be an iterable
        with precisely 4 elements in order.
        If content is not provided, a 4 element tuple, where all elements are
        None, is the default argument

        Args:
            content (iterable), where:
                [0] (AttrTypes) - attribute type
                [1] (CollationRule) - collation rule
                [2] (int) - index record size in bytes
                [3] (int) - index record size in clusters
            node_header (IndexNodeHeader) - the node header related to this index root
            idx_entry_list (list of IndexEntry)- list of index entries that belong to
                this index root
        '''
        self.attr_type, self.collation_rule, self.index_len_in_bytes, \
        self.index_len_in_cluster = content
        self.node_header = node_header
        self.index_entry_list = idx_entry_list

    @classmethod
    def get_static_content_size(cls):
        '''Returns the static size of the content never taking in consideration
        variable fields, for example, names.

        Returns:
            int: The size of the content, in bytes
        '''
        return cls._REPR.size

    @classmethod
    def create_from_binary(cls, binary_view):
        '''Creates a new object IndexRoot from a binary stream. The binary
        stream can be represented by a byte string, bytearray or a memoryview of the
        bytearray.

        Args:
            binary_view (memoryview of bytearray) - A binary stream with the
                information of an IndexRoot

        Returns:
            IndexRoot: New object using the binary stream as source
        '''
        content = cls._REPR.unpack(binary_view[:cls._REPR.size])
        nw_obj = cls()
        nw_obj.node_header = IndexNodeHeader.create_from_binary(binary_view[cls._REPR.size:])
        index_entry_list = []
        attr_type = AttrTypes(content[0]) if content[0] else None

        offset = cls._REPR.size + nw_obj.node_header.start_offset
        #loads all index entries related to the root node
        while True:
            entry = IndexEntry.create_from_binary(binary_view[offset:], attr_type)
            index_entry_list.append(entry)
            if entry.flags & IndexEntryFlags.LAST_ENTRY:
                break
            else:
                offset += entry.entry_len

        nw_obj.index_entry_list = index_entry_list
        nw_obj.attr_type, nw_obj.collation_rule, nw_obj.index_len_in_bytes, \
        nw_obj.index_len_in_cluster = attr_type, CollationRule(content[1]), \
            content[2], content[3]

        return nw_obj

    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + '(attr_type={!s}, collation_rule={}, index_len_in_bytes={}, index_len_in_cluster={}, node_header={}, index_entry_list={})'.format(
            self.attr_type, self.collation_rule, self.index_len_in_bytes,
            self.index_len_in_cluster, self.node_header, self.index_entry_list)

#******************************************************************************
# BITMAP ATTRIBUTE
#******************************************************************************
class Bitmap():
    '''Represents the bitmap attribute'''
    def __init__(self, bitmap_view):
        self._bitmap = bitmap_view.tobytes()

    #TODO write a function to allow query if a particular entry is allocated
    #TODO write a function to show all the allocated entries

    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + '(bitmap={})'.format(
            self._bitmap)

#******************************************************************************
# REPARSE_POINT ATTRIBUTE
#******************************************************************************
class JunctionOrMount():
    _REPR = struct.Struct("<4H")
    ''' Offset to target name - 2 (relative to 16th byte)
        Length of target name - 2
        Offset to print name - 2 (relative to 16th byte)
        Length of print name - 2
    '''
    def __init__(self, target_name=None, print_name=None):
        self.target_name, self.print_name = target_name, print_name

    @classmethod
    def create_from_binary(cls, binary_view):
        '''Creates a new object JunctionOrMount from a binary stream. The binary
        stream can be represented by a byte string, bytearray or a memoryview of the
        bytearray.

        Args:
            binary_view (memoryview of bytearray) - A binary stream with the
                information of an JunctionOrMount

        Returns:
            JunctionOrMount: New object using the binary stream as source
        '''
        content = cls._REPR.unpack(binary_view[:cls._REPR.size])
        repar_point_size = ReparsePoint.get_static_content_size()

        offset = repar_point_size + content[0]
        target_name = binary_view[offset:offset+content[1]].tobytes().decode("utf_16_le")
        offset = repar_point_size + content[2]
        print_name = binary_view[offset:offset+content[3]].tobytes().decode("utf_16_le")

        return cls(target_name, print_name)

    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + '(target_name={}, print_name={})'.format(
            self.target_name, self.print_name)

class ReparsePoint():
    _REPR = struct.Struct("<IH2x")
    ''' Reparse type flags - 4
            Reparse tag - 4 bits
            Reserved - 12 bits
            Reparse type - 2
        Reparse data length - 2
        Padding - 2
    '''
    def __init__(self, content=(None,)*5):
        '''Creates a IndexRoot object. The content has to be an iterable
        with precisely 5 elements in order.
        If content is not provided, a 5 element tuple, where all elements are
        None, is the default argument

        Args:
            content (iterable), where:
                [0] (ReparseType) - Reparse point type
                [1] (ReparseFlags) - Reparse point flags
                [2] (int) - reparse data length
                [3] (binary str) - guid (exists only in 3rd party reparse points)
                [4] (variable) - content of the reparse type
        '''
        self.reparse_type, self.reparse_flags, self.data_len, \
        self.guid, self.data = content

    @classmethod
    def get_static_content_size(cls):
        '''Returns the static size of the content never taking in consideration
        variable fields, for example, names.

        Returns:
            int: The size of the content, in bytes
        '''
        return cls._REPR.size

    @classmethod
    def create_from_binary(cls, binary_view):
        '''Creates a new object JunctionOrMount from a binary stream. The binary
        stream can be represented by a byte string, bytearray or a memoryview of the
        bytearray.

        Args:
            ReparsePoint (memoryview of bytearray) - A binary stream with the
                information of an JunctionOrMount

        Returns:
            ReparsePoint: New object using the binary stream as source
        '''
        content = cls._REPR.unpack(binary_view[:cls._REPR.size])
        nw_obj = cls()

        #reparse_tag (type, flags) data_len, guid, data
        nw_obj.reparse_flag = ReparseFlags((content[0] & 0xF0000000) >> 28)
        nw_obj.reparse_type = ReparseType(content[0] & 0x0000FFFF)
        guid = None #guid exists only in third party reparse points
        if nw_obj.reparse_flag & ReparseFlags.IS_MICROSOFT:#a microsoft tag
            if nw_obj.reparse_type is ReparseType.MOUNT_POINT or nw_obj.reparse_type is ReparseType.SYMLINK:
                data = JunctionOrMount.create_from_binary(binary_view[cls._REPR.size:])
            else:
                data = binary_view[cls._REPR.size:].tobytes()
        else:
            guid = binary_view[cls._REPR.size:cls._REPR.size+16].tobytes()
            data = binary_view[cls._REPR.size+len(guid):].tobytes()
        nw_obj.data_len, nw_obj.guid, nw_obj.data = content[1], guid, data

        return nw_obj

    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + '(reparse_flags={!s}, reparse_type={!s}, data_len={}, guid={}, data={})'.format(
            self.reparse_type, self.reparse_flags, self.data_len, self.guid, self.data)

#******************************************************************************
# EA_INFORMATION ATTRIBUTE
#******************************************************************************
class EaInformation():
    _REPR = struct.Struct("<2HI")
    ''' Size of Extended Attribute entry - 2
        Number of Extended Attributes which have NEED_EA set - 2
        Size of extended attribute data - 4
    '''
    def __init__(self, point_view):
        self.entry_len, self.ea_set_number, self.ea_size = \
            EaInformation._REPR.unpack(point_view[:EaInformation._REPR.size])

    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + '(entry_len={}, ea_set_number={}, ea_size={})'.format(
            self.entry_len, self.ea_set_number, self.ea_size)

#******************************************************************************
# EA ATTRIBUTE
#******************************************************************************
#TODO implement EA attribute
class Ea():
    def __init__(self, bin_view):
        pass

    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + "()"

#******************************************************************************
# SECURITY_DESCRIPTOR ATTRIBUTE
#******************************************************************************
#TODO implement SECURITY_DESCRIPTOR attribute
class SecurityDescriptor():
    def __init__(self, bin_view):
        pass

    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + "()"


#******************************************************************************
# LOGGED_TOOL_STREAM ATTRIBUTE
#******************************************************************************
class LoggedToolStream():
    #TODO implement the know cases of this attribute
    def __init__(self, bin_view):
        '''Initialize the class. Expects the binary_view that represents the
        content. Size information is derived from the content.
        '''
        self.content = bin_view.tobytes()

    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + '(content={})'.format(
            self.content)
