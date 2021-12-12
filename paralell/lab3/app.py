import time
from components.videostream import InputVideoStream
from components.core import Processor
from components.config import ParamsContainer
from components.signal_process import BufferTimer
from components.app_extensions.plots import *
from components.app_extensions.savers import *
from components.app_extensions.BaseToggler import BaseToggler
import copy


__author__ = "Sergii Nikolaiev"

"""
MainController class performs all connections of components and controls data flow
"""


try:
    basestring
except NameError:
    basestring = str


class FPSTimer(BaseToggler):
    """
    Measures time elapsed between 2 frames and outputs FPS
      is used for testing purposes mostly
      no hard integration and dependencies with the system
    """

    def __init__(self):
        BaseToggler.__init__(self)
        self.fps_last_time = 0

    def do_work(self, handler):
        if self.state:
            if self.fps_last_time:
                end = time.time()
                d = end - self.fps_last_time
                fps = 0
                if d > 0:
                    fps = 1.0 / d
                print("FPS:{0:.2f}".format(fps) + " Elapsed:" + str(d))
        self.fps_last_time = time.time()


class MainWndFullScreenModifier:
    """
    Makes video frame full screen mode OR windowed mode
    """

    def __init__(self, wnd_name):
        self.state = False
        self.wnd_name = wnd_name

    def toggle(self):
        self.state = not self.state
        print("Full screen " + str(self.state))
        cv2.setWindowProperty(self.wnd_name, 0, float(self.state))


class RecordingStrategy:
    """
    Stores structure of type {"Frame_number":15, "EventsAray":[ start_recording, show_form1 ... ] }
    """

    def __init__(self, frame_event_arr=dict()):
        self.frame_event_arr = frame_event_arr

    def check_events(self, frame_num):
        if frame_num in self.frame_event_arr:
            for delegate in self.frame_event_arr[frame_num]:
                delegate()


class MainController:
    def __init__(self):
        """
        Initial settings of all logic
        """

        # stream = 1
        STREAM_NUM = 0

        stream = STREAM_NUM

        is_ip_cam = 0
        do_save = 0

        params = ParamsContainer()
        self.video_st = InputVideoStream(
            stream, set_cam_WxH=params.frame_WxH
        )  # (1280, 720)) #(800, 600)#, skip_n_frames=50)#

        # #################### Frame Viewer  ##########################
        self.main_wnd_name = (
            "Viewer: Press ESC to exit"  # name is needed for extensions (FullScreen)
        )
        cv2.namedWindow(self.main_wnd_name, flags=0)
        self.frame = None
        self.orig_frame = None
        # #################### Init processor #########################

        # params.recorded_video_file_name = pref+"res.avi"
        params.frame_WxH = (self.video_st.width, self.video_st.height)
        is_stream_from_cam = (not isinstance(stream, basestring)) or is_ip_cam

        fps = 25
        if is_stream_from_cam:
            print("Live stream - disabling video_fps")
        else:
            print("Processing Recording")
            fps = self.video_st.fps
        params.timer = BufferTimer(is_stream_from_cam, fps_emulation_rate=fps)

        # params.buffer_length = 5*fps  # Buffer size is 5 sec
        # params.max_face_losses_allowed = 5*fps  # Kill pipe in 10 sec if face is lost
        self.processor = Processor(params)

        # ####################### Components ###########################
        hrv_plot = HRVPlot()  # widgets_offsets=params.widgets_offsets)
        stat_saver = TXTStatsSaver(1)
        pulse_saver = PulseSaver(1)
        raw_bgr_sig_saver = RawChannelsSaver(1)
        fps_timer = FPSTimer()
        frames_saver = FrameSaver(
            filename=params.recorded_video_file_name,
            is_on=do_save,
            fps=fps,
            video_WxH=params.frame_WxH,
        )
        full_scr = MainWndFullScreenModifier(self.main_wnd_name)
        bpm = BPMPlot(0)  # Shows inner system buffers in black window

        # Event Controls
        self.key_controls = {
            chr(27): self.finalize,
            "r": fps_timer.toggle,
            "f": full_scr.toggle,
            "s": frames_saver.toggle,
            # 'c': bpm.reset,
            "d": bpm.toggle,
            "S": stat_saver.toggle,
            "p": pulse_saver.toggle,
            "h": hrv_plot.toggle,
            # '$': raw_bgr_sig_saver.toggle,
            "1": hrv_plot.toggle_signal,
            "@": hrv_plot.toggle_mhr,
            "2": hrv_plot.toggle_rr,
            "w": hrv_plot.toggle_rr_orig,
            "3": hrv_plot.toggle_hr_plot,
            "e": hrv_plot.toggle_hr_plot_orig,
            "4": hrv_plot.toggle_si,
            "5": hrv_plot.toggle_sp,
            "6": hrv_plot.toggle_si_plot,
            #   '6': hrv_plot.toggle_ic,
            #   '7': hrv_plot.toggle_isca,
            #   '8': hrv_plot.toggle_vb,
            "l": hrv_plot.toggle_lightness,
            "9": hrv_plot.toggle_testing_info_panel,
            #   'a': hrv_plot.toggle_liveness_detector,
            # '4': hrv_plot.toggle_peaks,
            "0": hrv_plot.toggle_info,
            "-": hrv_plot.toggle_face,
            # '0': hrv_plot.toggle_noise_sig_ratio #!
        }
        self.loop_event_handlers = [
            fps_timer.do_work,
            hrv_plot.do_work,
            bpm.do_work,
            stat_saver.do_work,
            pulse_saver.do_work,
            raw_bgr_sig_saver.do_work,
            frames_saver.do_work,
        ]

        self.finalise_list = [frames_saver.finalizer]

        # ################# Recording video strategy ###################
        # strat_news_lady = {int(2 * fps): [frames_saver.toggle],  # Start recording
        #                    int(3 * fps): [hrv_plot.toggle_info],  # Show text
        #                    int(8 * fps): [hrv_plot.toggle_info, hrv_plot.toggle_signal, hrv_plot.toggle_hr_plot],
        #                    # hide text, show signal
        #                    # int(8*fps)+1: [hrv_plot.toggle_hr_plot], #show heart rate
        #
        #                    int(32 * fps): [hrv_plot.toggle_signal, hrv_plot.toggle_hr_plot, hrv_plot.toggle_hrinfo],
        #                    # hide sig and hr show final info
        #
        #                    int(36 * fps): [hrv_plot.toggle_hrinfo, frames_saver.toggle, self.finalize]
        #                    # hide final info , stop recording, stop video
        #                    }
        # strat = strat_news_lady
        strat = dict()  # #!!!# -> No recording
        strat = {5: [full_scr.toggle]}  # make full screen after 1st captured frame
        self.rec_strategy = RecordingStrategy(strat)
        self.cur_frame_cnt = 0

    def finalize(self):
        print("exiting application...")
        self.video_st.close_stream()
        # Stop components
        for f in self.finalise_list:
            f()
        cv2.destroyAllWindows()
        exit()

    def main_loop(self):
        """
        Single iteration of the application's main loop.
        """
        frame = self.video_st.read_frame()
        if not self.video_st.read_successful():
            return

        self.frame = frame  # for video saver
        self.orig_frame = copy.copy(frame)  # for video saver

        self.frame = self.processor.process_frame(frame)

        # Run all loop_event_handlers
        [l(self) for l in self.loop_event_handlers]

        cv2.imshow(self.main_wnd_name, self.frame)

        # handle any key presses
        self.key_handler()

        # Video recording strategy
        self.rec_strategy.check_events(self.cur_frame_cnt)
        self.cur_frame_cnt += 1

    def key_handler(self):
        """
        Handle keystrokes, as set at the bottom of __init__()
        A plotting or camera frame window must have focus for keypresses to be
        detected.
        """
        key = chr(cv2.waitKey(1) & 255)  # wait for keypress for 1 ms
        if key in self.key_controls.keys():
            self.key_controls[key]()


if __name__ == "__main__":
    App = MainController()
    while True:
        App.main_loop()
        if not App.video_st.read_successful():
            print("Stream has finished")
            break
    App.finalize()
