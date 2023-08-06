class Track:
    """
    A track object summarize an activity

        init args :
        filepath : , 
        platform='garmin', 
        athlete='unknown', 
        activity_id='unknown' (platform id), 
        type='unkown' (activity type)

    attributes :
        points (dataframe)   : timestamp, lat, lon, ...
        features (dict) : global features
            ['activity_id', 'activity_name', 'activity_type', 'athlete', 'date',
            'device', 'distance', 'duration', 'elevationGain', 'has_po', 'has_tcx',
            'has_hr', 'startLatitude', 'startLongitude', 'startTimeGMT',
            'race_name', 'race_id', 'avHR', 'isarun',
            record_data  (device, platform, ...)
        
    methods :
        parse :
        get_google_elevation :
        get_speed :
        get_run_po :
        get_ta :
    """

    def __init__(self, filepath='tcx_folder', platform='garmin', athlete='unknown', activity_id='unknown', type='unkown'):
        self.platform = platform
        
        
        """"

"""
