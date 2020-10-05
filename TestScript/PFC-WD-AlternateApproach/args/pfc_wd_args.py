def add_pfc_wd_args(parser):
    """
        Adding arguments required for PFC WD test cases
       Args:
            parser: pytest parser object
        Returns:
            None
    """
    pfc_wd_group = parser.getgroup("PFC WD test suite options")

    pfc_wd_group.addoption(
        "--start_delay",
        action="store",
        type=int,
        default=1,
        help="Time to delay traffic start after initiating the traffic flow",
    )

    pfc_wd_group.addoption(
        "--traffic_duration",
        action="store",
        type=int,
        default=3,
        help="Traffic duration time",
    )

    pfc_wd_group.addoption(
        "--pause_line_rate",
        action="store",
        type=int,
        default=50,
        help="Pause Storm line rate",
    )

    pfc_wd_group.addoption(
        "--traffic_line_rate",
        action="store",
        type=int,
        default=50,
        help="Traffic Line Rate",
    )

    pfc_wd_group.addoption(
        "--bw_multiplier",
        action="store",
        type=int,
        default=1000000,
        help="Bandwidth Mutliplier to convert Mbps to bps",
    )

    pfc_wd_group.addoption(
        "--frame_size",
        action="store",
        type=int,
        default=1024,
        help="Frame Size to be set for Traffic stream",
    )

    pfc_wd_group.addoption(
        "--t_start_pause",
        action="store",
        type=int,
        default=5,
        help="Time at Pause Storm to be started after traffic starts",
    )

    pfc_wd_group.addoption(
        "--t_stop_pause",
        action="store",
        type=int,
        default=10,
        help="Time at Pause Storm to be stopped after traffic starts \
             time should be greater than t_start_pause",
    )

    pfc_wd_group.addoption(
        "--t_stop_traffic",
        action="store",
        type=int,
        default=15,
        help="Time at traffic should be stopped",
    )

    pfc_wd_group.addoption(
        "--storm_detection_time",
        action="store",
        type=int,
        default=400,
        help="Pause Storm Detection Time",
    )

    pfc_wd_group.addoption(
        "--storm_restoration_time",
        action="store",
        type=int,
        default=2000,
        help="Pause Storm Restoration Time",
    )