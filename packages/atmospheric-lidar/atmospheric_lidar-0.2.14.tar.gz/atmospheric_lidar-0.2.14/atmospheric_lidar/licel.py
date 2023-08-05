import datetime
import logging
import copy

import numpy as np
import pytz

from generic import BaseLidarMeasurement, LidarChannel

logger = logging.getLogger(__name__)

licel_file_header_format = ['Filename',
                            'StartDate StartTime EndDate EndTime Altitude Longtitude Latitude ZenithAngle',
                            # Appart from Site that is read manually
                            'LS1 Rate1 LS2 Rate2 DataSets', ]
licel_file_channel_format = 'Active AnalogPhoton LaserUsed DataPoints 1 HV BinW Wavelength d1 d2 d3 d4 ADCbits NShots Discriminator ID'

c = 299792458.0  # Speed of light


class LicelFile:
    """ A class representing a single binary Licel file. """

    def __init__(self, file_path, use_id_as_name=False, licel_timezone="UTC"):
        """
        This is run when creating a new object.
        
        Parameters
        ----------
        file_path : str
           The path to the Licel file.
        use_id_as_name : bool
           If True, the transient digitizer name (e.g. BT0) is used as a channel
           name. If False, a more descriptive name is used (e.g. '01064.o_an').
        licel_timezone : str
           The timezone of dates found in the Licel files. Should match the available
           timezones in the TZ database. 
        """
        self.filename = file_path
        self.use_id_as_name = use_id_as_name
        self.start_time = None
        self.stop_time = None
        self.licel_timezone = licel_timezone
        self._import_file(file_path)
        self.calculate_physical()

    def calculate_physical(self):
        """ Calculate physical quantities from raw data for all channels in the file. """
        for channel in self.channels.itervalues():
            channel.calculate_physical()

    def _import_file(self, file_path):
        """ Read the content of the Licel file.
        
        Parameters
        ----------
        file_path : str
           The path to the Licel file.
        """
        channels = {}

        with open(file_path, 'rb') as f:

            self.read_header(f)

            # Check the complete header is read
            f.readline()

            # Import the data
            for current_channel_info in self.channel_info:
                raw_data = np.fromfile(f, 'i4', int(current_channel_info['DataPoints']))
                a = np.fromfile(f, 'b', 1)
                b = np.fromfile(f, 'b', 1)

                if (a[0] != 13) | (b[0] != 10):
                    logging.warning("No end of line found after record. File could be corrupt: %s" % file_path)
                channel = LicelFileChannel(current_channel_info, raw_data, self.duration(),
                                           use_id_as_name=self.use_id_as_name)

                channel_name = channel.channel_name

                if channel_name in channels.keys():
                    # If the analog/photon naming scheme is not enough, find a new one!
                    raise IOError('Trying to import two channels with the same name')

                channels[channel_name] = channel

        self.channels = channels

    def read_header(self, f):
        """ Read the header of an open Licel file. 
        
        Parameters
        ----------
        f : file-like object
           An open file object.
        """
        # Read the first 3 lines of the header
        raw_info = {}
        channel_info = []

        # Read first line
        raw_info['Filename'] = f.readline().strip()

        # Read second line
        second_line = f.readline()

        # Many Licel files don't follow the licel standard. Specifically, the
        # measurement site is not always 8 characters, and can include white
        # spaces. For this, the site name is detect everything before the first 
        # date. For efficiency, the first date is found by the first '/'.
        # e.g. assuming a string like 'Site name 01/01/2010 ...' 

        site_name = second_line.split('/')[0][:-2]
        clean_site_name = site_name.strip()
        raw_info['Site'] = clean_site_name
        raw_info.update(self.match_lines(second_line[len(clean_site_name) + 1:], licel_file_header_format[1]))

        # Read third line
        third_line = f.readline()
        raw_info.update(self.match_lines(third_line, licel_file_header_format[2]))

        # Update the object properties based on the raw info
        start_string = '%s %s' % (raw_info['StartDate'], raw_info['StartTime'])
        stop_string = '%s %s' % (raw_info['EndDate'], raw_info['EndTime'])
        date_format = '%d/%m/%Y %H:%M:%S'

        try:
            logger.debug('Creating timezone object %s' % self.licel_timezone)
            timezone = pytz.timezone(self.licel_timezone)
        except:
            raise ValueError("Cloud not create time zone object %s" % self.licel_timezone)

        # According to pytz docs, timezones do not work with default datetime constructor.
        local_start_time = timezone.localize(datetime.datetime.strptime(start_string, date_format))
        local_stop_time = timezone.localize(datetime.datetime.strptime(stop_string, date_format))

        # Only save UTC time.
        self.start_time = local_start_time.astimezone(pytz.utc)
        self.stop_time = local_stop_time.astimezone(pytz.utc)

        self.latitude = float(raw_info['Latitude'])
        self.longitude = float(raw_info['Longtitude'])

        # Read the rest of the header.
        for c1 in range(int(raw_info['DataSets'])):
            channel_info.append(self.match_lines(f.readline(), licel_file_channel_format))

        self.raw_info = raw_info
        self.channel_info = channel_info

    def duration(self):
        """ Return the duration of the file. 
        
        Returns
        -------
        : float
           The duration of the file in seconds.
        """
        dt = self.stop_time - self.start_time
        return dt.seconds

    @staticmethod
    def match_lines(f1, f2):
        list1 = f1.split()
        list2 = f2.split()

        if len(list1) != len(list2):
            logging.debug("Channel parameter list has different length from licel specifications.")
            logging.debug("List 1: %s" % list1)
            logging.debug("List 2: %s" % list2)
        combined = zip(list2, list1)
        combined = dict(combined)
        return combined


class LicelFileChannel:
    """ A class representing a single channel found in a single Licel file."""

    def __init__(self, raw_info, raw_data, duration, use_id_as_name=False):
        """
        This is run when creating a new object.

        Parameters
        ----------
        raw_info : dict
           A dictionary containing raw channel information.
        raw_data : dict
           An array with raw channel data.    
        duration : float
           Duration of the file, in seconds
        use_id_as_name : bool
           If True, the transient digitizer name (e.g. BT0) is used as a channel
           name. If False, a more descriptive name is used (e.g. '01064.o_an').
        """
        self.raw_info = raw_info
        self.raw_data = raw_data
        self.duration = duration
        self.use_id_as_name = use_id_as_name
        self.adcbits = int(raw_info['ADCbits'])
        self.active = int(raw_info['Active'])
        self.analog_photon = raw_info['AnalogPhoton']
        self.bin_width = float(raw_info['BinW'])
        self.data_points = int(raw_info['DataPoints'])

        self.hv = float(raw_info['HV'])
        self.id = raw_info['ID']
        self.laser_user = int(raw_info['LaserUsed'])
        self.number_of_shots = int(raw_info['NShots'])
        self.wavelength_str = raw_info['Wavelength']

        if self.is_analog:
            self.discriminator = float(raw_info['Discriminator']) * 1000  # Analog range in mV
        else:
            self.discriminator = float(raw_info['Discriminator'])

    @property
    def wavelength(self):
        """ Property describing the nominal wavelength of the channel.
        
        Returns
        -------
        : int or None
           The integer value describing the wavelength. If no raw_info have been provided, 
           returns None.
        """
        wavelength = self.wavelength_str.split('.')[0]
        return int(wavelength)

    @property
    def channel_name(self):
        """
        Construct the channel name adding analog photon info to avoid duplicates

        If use_id_as_name is True, the channel name will be the transient digitizer ID (e.g. BT01).
        This could be useful if the lidar system has multiple telescopes, so the descriptive name is
        not unique.
        
        Returns
        -------
        channel_name : str
           The channel name
        """
        if self.use_id_as_name:
            channel_name = self.id
        else:
            acquisition_type = self.analog_photon_string
            channel_name = "%s_%s" % (self.wavelength_str, acquisition_type)
        return channel_name

    @property
    def analog_photon_string(self):
        """ Convert the analog/photon flag found in the Licel file to a proper sting.

        Returns
        -------
        string : str
           'an' or 'ph' string, for analog or photon-counting channel respectively.
        """
        if self.analog_photon == '0':
            string = 'an'
        else:
            string = 'ph'
        return string

    def calculate_physical(self):
        """ Calculate physically-meaningful data from raw channel data:
        
        * In case of analog signals, the data are converted to mV.
        * In case of photon counting signals, data are stored as number of photons.
        
        In addition, some ancillary variables are also calculated (z, dz, number_of_bins). 
        """
        data = self.raw_data

        norm = data / float(self.number_of_shots)
        dz = float(self.raw_info['BinW'])

        if self.raw_info['AnalogPhoton'] == '0':
            # If the channel is in analog mode
            ADCrange = self.discriminator * 1000  # Value in mV
            channel_data = norm * ADCrange / ((2 ** self.adcbits) - 1)

            # print ADCb, ADCRange,cdata,norm
        else:
            # If the channel is in photoncounting mode
            # Frequency deduced from range resolution! (is this ok?)
            # c = 300 # The result will be in MHZ
            # SR  = c/(2*dz) # To account for pulse folding
            # channel_data = norm*SR
            # CHANGE:
            # For the SCC the data are needed in photons
            channel_data = norm * self.number_of_shots
            # print res,c,cdata,norm

        # Calculate Z

        self.z = np.array([dz * bin_number + dz / 2.0 for bin_number in range(self.data_points)])
        self.dz = dz
        self.data = channel_data

    @property
    def is_analog(self):
        return self.analog_photon == '0'


class LicelLidarMeasurement(BaseLidarMeasurement):

    def __init__(self, file_list=None, use_id_as_name=False, licel_timezone='UTC'):
        self.raw_info = {}  # Keep the raw info from the files
        self.durations = {}  # Keep the duration of the files
        self.laser_shots = []

        self.use_id_as_name = use_id_as_name
        self.licel_timezone = licel_timezone
        super(LicelLidarMeasurement, self).__init__(file_list)

    def _import_file(self, filename):
        if filename in self.files:
            logger.warning("File has been imported already: %s" % filename)
        else:
            logger.debug('Importing file {0}'.format(filename))
            current_file = LicelFile(filename, use_id_as_name=self.use_id_as_name, licel_timezone=self.licel_timezone)
            self.raw_info[current_file.filename] = current_file.raw_info
            self.durations[current_file.filename] = current_file.duration()

            file_laser_shots = []

            for channel_name, channel in current_file.channels.items():
                if channel_name not in self.channels:
                    self.channels[channel_name] = LicelChannel()
                self.channels[channel_name].append_file(current_file.start_time, channel)

            self.laser_shots.append(file_laser_shots)
            self.files.append(current_file.filename)

    def append(self, other):

        self.start_times.extend(other.start_times)
        self.stop_times.extend(other.stop_times)

        for channel_name, channel in self.channels.items():
            channel.append(other.channels[channel_name])

    def _get_duration(self, raw_start_in_seconds):
        """ Return the duration for a given time scale. If only a single
        file is imported, then this cannot be guessed from the time difference
        and the raw_info of the file are checked.
        """

        if len(raw_start_in_seconds) == 1:  # If only one file imported
            duration = self.durations.itervalues().next()  # Get the first (and only) raw_info
            duration_sec = duration
        else:
            duration_sec = np.diff(raw_start_in_seconds)[0]

        return duration_sec

    def _get_custom_variables(self, channel_names):

        daq_ranges = np.ma.masked_all(len(channel_names))
        for n, channel_name in enumerate(channel_names):
            channel = self.channels[channel_name]
            if channel.is_analog:
                unique_values = list(set(channel.discriminator))
                if len(unique_values) > 1:
                    logger.warning('More than one discriminator levels for channel {0}: {1}'.format(channel_name, unique_values))
                daq_ranges[n] = unique_values[0]

        laser_shots = []
        for channel_name in channel_names:
            channel = self.channels[channel_name]
            laser_shots.append(channel.laser_shots)

        laser_shots = np.array(laser_shots).T

        params = [{
            "name": "DAQ_Range",
            "dimensions": ('channels',),
            "type": 'd',
            "values": daq_ranges,
        }, {
            "name": "Laser_Shots",
            "dimensions": ('time', 'channels',),
            "type": 'i',
            "values": laser_shots,
        },
        ]

        return params

    def _get_custom_global_attributes(self):
        """
        NetCDF global attributes that should be included
        in the final NetCDF file.

        Currently the method assumes that all files in the measurement object have the same altitude, lat and lon
        properties.
        """
        logger.debug('Setting custom global attributes')
        logger.debug('raw_info keys: {0}'.format(self.raw_info.keys()))

        params = [{
            "name": "Altitude_meter_asl",
            "value": float(self.raw_info[self.files[0]]["Altitude"])
        }, {
            "name": "Latitude_degrees_north",
            "value": float(self.raw_info[self.files[0]]["Latitude"])
        }, {
            "name": "Longitude_degrees_east",
            "value": float(self.raw_info[self.files[0]]["Longtitude"])
        },
        ]

        return params

    def subset_by_channels(self, channel_subset):
        """
        Create a measurement object containing only a subset of  channels.

        This method overrides the parent method to add some licel-spefic parameters to the new object.

        Parameters
        ----------
        channel_subset : list
           A list of channel names (str) to be included in the new measurement object.

        Returns
        -------
        m : BaseLidarMeasurements object
           A new measurements object
        """
        new_measurement = super(LicelLidarMeasurement, self).subset_by_channels(channel_subset)

        new_measurement.raw_info = copy.deepcopy(self.raw_info)
        new_measurement.durations = copy.deepcopy(self.durations)
        new_measurement.laser_shots = copy.deepcopy(self.laser_shots)

        return new_measurement

    def subset_by_time(self, channel_subset):
        """
        Subsetting by time does not work yet with Licel files.

        This requires changes in generic.py
        """
        raise NotImplementedError("Subsetting by time, not yet implemented for Licel files.")
        

class LicelChannel(LidarChannel):

    def __init__(self):
        self.name = None
        self.resolution = None
        self.points = None
        self.wavelength = None
        self.laser_used = None

        self.rc = []
        self.raw_info = []
        self.laser_shots = []
        self.duration = []
        self.number_of_shots = []
        self.discriminator = []
        self.hv = []
        self.data = {}

    def append_file(self, file_start_time, file_channel):
        """ Append file to the current object """

        self._assign_unique_property('name', file_channel.channel_name)
        self._assign_unique_property('resolution', file_channel.dz)
        self._assign_unique_property('wavelength', file_channel.wavelength)
        self._assign_unique_property('points', file_channel.data_points)
        self._assign_unique_property('adcbits', file_channel.adcbits)
        self._assign_unique_property('active', file_channel.active)
        self._assign_unique_property('laser_user', file_channel.laser_user)
        self._assign_unique_property('adcbints', file_channel.adcbits)
        self._assign_unique_property('analog_photon_string', file_channel.analog_photon_string)

        self.binwidth = self.resolution * 2. / c  # in seconds
        self.z = file_channel.z

        self.data[file_start_time] = file_channel.data
        self.raw_info.append(file_channel.raw_info)
        self.laser_shots.append(file_channel.number_of_shots)
        self.duration.append(file_channel.duration)
        self.number_of_shots.append(file_channel.number_of_shots)
        self.discriminator.append(file_channel.discriminator)
        self.hv.append(file_channel.hv)

    def _assign_unique_property(self, property_name, value):

        current_value = getattr(self, property_name, None)

        if current_value is None:
            setattr(self, property_name, value)
        else:
            if current_value != value:
                raise ValueError('Cannot combine channels with different values of {0}.'.format(property_name))

    @property
    def is_analog(self):
        return self.analog_photon_string == 'an'

    @property
    def is_photon_counting(self):
        return self.analog_photon_string == 'ph'

    def __unicode__(self):
        return "<Licel channel: %s>" % self.name

    def __str__(self):
        return unicode(self).encode('utf-8')
