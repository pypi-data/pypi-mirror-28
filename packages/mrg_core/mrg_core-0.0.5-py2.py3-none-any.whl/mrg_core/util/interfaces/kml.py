"""
   Meteor KML file class module.
"""
import logging


class MeteorKML(object):
    """Creates a Google Earth KML file for a single meteor, once a maximum of
    two trajectories and two stations are provided.

    Parameters
    ----------
    path: str
       the kml file path to where the contents of the class instance shall
       be written. Optional.

    Raises
    ------
    KeyError
        if neither the ``path`` argument of the initialization method nor the
        ``path`` argument of the save method are provided when trying to
        create the Google Earth KML file.
    OverflowError
       if trying to set either 'trajectory' or 'station' more than twice.
    ValueError
       if trying to set item other than 'trajectory' or 'station'.

    Examples
    --------
    >>> from datetime import datetime
    >>> kml = MeteorKML('initial_file_name.kml')
    >>> kml['station'] = ('ICC7', 10.858890, 45.697498, 1208)
    >>> kml['trajectory'] = [
    ...     (datetime(2017, 1, 20, 12, 56, 1), 10.8, 45.6, 100000.0),
    ...     (datetime(2017, 1, 20, 12, 56, 2), 10.7, 45.7, 98000.3)]
    >>> # Print the KML XML file to stdout
    >>> print(kml)
    >>> # Save the KML XML file to the initially provide file name
    >>> kml.save()
    >>> # Save the KML XML file to a different file
    >>> kml.save('/path/to/new_file_name.kml')

    Notes
    -----
    If the ``path`` argument is provided both in the initialization method and
    in the save method, the later will be used to create the Google Earth KML
    file.

    """
    # Protected constant defining the different colors to use in KML colour
    # tags
    _colors = ['ff00ff00', 'ff0000ff']

    # Protected constant defining the XML sections required for the
    # description of a station location: {0}: color; {1}: name; {2}: longitude
    # {3}: latitude; {4}: altitude.
    _station_str = ("""
<Style id="station_{1}">
  <IconStyle>
     <color>{0}</color>
     <scale>1.8</scale>
     <Icon>
       <href>
        http://maps.google.com/mapfiles/kml/shapes/placemark_square.png
       </href>
     </Icon>
  </IconStyle>
  <LabelStyle><scale>1.0</scale></LabelStyle>
</Style>

<Placemark id="{1}">
  <name>{1}</name>
  <styleUrl>#station_{1}</styleUrl>
  <Point>
    <coordinates>{2},{3},{4}</coordinates>
    <altitudeMode>absolute</altitudeMode>
  </Point>
</Placemark>""")

    # Protected constant defining the XML sections required for the
    # description of the trajectory styles: {0}: trajectory number;
    # {1}: color.
    _t_style_str = ("""
<Style id="traject_{0}">
    <IconStyle>
        <color>{1}</color>
        <scale>0.75</scale>
        <Icon>
          <href>
            http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png
          </href>
        </Icon>
    </IconStyle>
    <LabelStyle><scale>0.75</scale></LabelStyle>
</Style>""")

    # Protected constant defining the XML sections required for the
    # description of a trajectory point: {0}: trajectory style number;
    # {1}: time in ISO format; {2}: longitude; {3}: latitude; {4}: altitude.
    _point_str = ("""
<Placemark>
    <styleUrl>#traject_{0}</styleUrl>
    <description>
      {1}
      Altitude: {4}
      Longitude: {2}
      Latitude: {3}
    </description>
    <TimeStamp><when>{1}</when></TimeStamp>
    <Point>
        <coordinates>{2},{3},{4}</coordinates>
        <altitudeMode>absolute</altitudeMode>
        <extrude>1</extrude>
    </Point>
</Placemark>""")

    def __init__(self, path=None):
        self._path = path
        self._trajectory = []
        self._station = []

    def __setitem__(self, key, value):
        """Assigns to the protected trajectory and station attributes the
        data provided in the value parameter, for a maximum of two iterations,
        if the provided key is one of the protected attributes"""

        if key not in ['trajectory', 'station']:
            msg = ("'Class MeteorKML does not "
                   "contain '{}' attribute").format(key)
            logging.error(msg)
            raise ValueError(msg)
        private = '_{}'.format(key)
        if len(self.__dict__[private]) == 2:
            msg = "Attribute '{}' already contains two elements".format(key)
            logging.error(msg)
            raise OverflowError(msg)

        self.__dict__[private].append(value)

    def __str__(self):
        """Converts the contents of the protected trajectory and station
        attributes to a string following the XML file format."""
        kml = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<kml xmlns="http://www.opengis.net/kml/2.2"',
               '     xmlns:gx="http://www.google.com/kml/ext/2.2"',
               '     xmlns:kml="http://www.opengis.net/kml/2.2"',
               '     xmlns:atom="http://www.w3.org/2005/Atom">',
               '',
               '<Document>']

        # Add the trajectory data
        for i, trajectory in enumerate(self._trajectory):
            kml.append(self._t_style_str.format(i + 1, self._colors[i]))
            for point in trajectory:
                kml.append(self._point_str.format(i + 1, point[0].isoformat(),
                                                  *point[1:]))

        for i, station in enumerate(self._station):
            kml.append(self._station_str.format(self._colors[i], *station))

        # Add the KML file
        kml.extend(['</Document>', '</kml>'])
        return '\n'.join(kml)

    def save(self, path=None):
        """
        Saves the contents of the class instance to a file whose path is given
        either through the class initialization parameter ``path`` or this
        method's call parameter ``path``.  Note that the method's parameter
        takes precedence over the class' initialization parameter.

        Parameters
        ----------
        path: str
           the kml file path to where the contents of the class instance shall
           be written.

        Raises
        ------
        KeyError
           if neither the ``path`` attribute of the class instance, nor the
           ``path`` parameter of the save method have been provided.

        """
        if not path:
            path = self._path

        if path:
            with open(path, 'w') as fhandle:
                fhandle.write(self.__str__())
        else:
            msg = ("Neither the 'path' attribute of the class, nor the 'path'"
                   " parameter of the save method have been provided.")
            logging.error(msg)
            raise KeyError(msg)
