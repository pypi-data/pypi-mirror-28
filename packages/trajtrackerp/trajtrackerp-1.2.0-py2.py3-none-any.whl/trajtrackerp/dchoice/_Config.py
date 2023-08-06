"""
Configuration of a discrete-choice experiment

@author: Dror Dotan
@copyright: Copyright (c) 2017, Dror Dotan

This file is part of TrajTracker.

TrajTracker is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

TrajTracker is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with TrajTracker.  If not, see <http://www.gnu.org/licenses/>.
"""

from enum import Enum
import expyriment as xpy
# noinspection PyProtectedMember
from trajtrackerp.common._BaseConfig import BaseConfig, FINGER_STARTED_MOVING
from trajtrackerp import sounds_dir


class Config(BaseConfig):

    def __init__(self, experiment_id, data_source, max_movement_time,
                 use_text_targets=True, use_generic_targets=False,

                 fixation_type='cross', hide_fixation_event=FINGER_STARTED_MOVING, fixation_text=None,
                 fixzoom_box_size=(40, 40), fixzoom_dot_radius=3,
                 fixzoom_dot_colour=xpy.misc.constants.C_GREY,
                 fixzoom_zoom_duration=0.2, fixzoom_stay_duration=0.1,
                 fixzoom_show_event=None, fixzoom_start_zoom_event=None,

                 text_target_height=0.6, shuffle_trials=True,
                 log_stimulus_onset_offset=False,
                 min_movement_time=0.2, speed_guide_enabled=False, min_inst_speed=10,
                 grace_period=0.3, max_zigzags=8, max_offscreen_duration=0,
                 save_results=True, sounds_dir=sounds_dir,
                 stimulus_then_move=False, finger_must_start_upwards=True,
                 finger_moves_min_time=None, finger_moves_max_time=None,
                 start_point_size=(40, 30), start_point_tilt=0,
                 start_point_colour=xpy.misc.constants.C_GREY,

                 confidence_rating=False,

                 resp_btn_size=(0.05, 0.1), resp_btn_positions=None,
                 resp_btn_colours=xpy.misc.constants.C_GREY,
                 resp_btn_font_name="Arial", resp_btn_font_size=16,
                 resp_btn_texts=None,
                 resp_btn_text_colour=xpy.misc.constants.C_WHITE,

                 feedback_stim_type=None, feedback_place='button', feedback_select_by='response',
                 feedback_btn_colours=None, feedback_duration=0.2,
                 feedback_rect_size=None, feedback_stim_position=None,
                 feedback_pictures=None):

        super(Config, self).__init__(
            experiment_id=experiment_id,
            data_source=data_source,
            max_movement_time=max_movement_time,
            use_text_targets=use_text_targets,
            use_generic_targets=use_generic_targets,
            fixation_type=fixation_type,
            hide_fixation_event=hide_fixation_event,
            fixation_text=fixation_text,
            fixzoom_box_size=fixzoom_box_size,
            fixzoom_dot_radius=fixzoom_dot_radius,
            fixzoom_dot_colour=fixzoom_dot_colour,
            fixzoom_zoom_duration=fixzoom_zoom_duration,
            fixzoom_stay_duration=fixzoom_stay_duration,
            fixzoom_show_event=fixzoom_show_event,
            fixzoom_start_zoom_event=fixzoom_start_zoom_event,
            text_target_height=text_target_height,
            shuffle_trials=shuffle_trials,
            log_stimulus_onset_offset=log_stimulus_onset_offset,
            min_movement_time=min_movement_time,
            speed_guide_enabled=speed_guide_enabled,
            min_inst_speed=min_inst_speed,
            grace_period=grace_period,
            max_zigzags=max_zigzags,
            max_offscreen_duration=max_offscreen_duration,
            save_results=save_results,
            sounds_dir=sounds_dir,
            stimulus_then_move=stimulus_then_move,
            finger_must_start_upwards=finger_must_start_upwards,
            finger_moves_min_time=finger_moves_min_time,
            finger_moves_max_time=finger_moves_max_time,
            start_point_size=start_point_size,
            start_point_tilt=start_point_tilt,
            start_point_colour=start_point_colour,
            confidence_rating=confidence_rating,
        )


        #----- Configuration of response buttons -----

        #: Size of the response buttons (width, height).
        self.resp_btn_size = resp_btn_size

        #: Position of the response button. This can be either of:
        #:
        #: - (x,y) tuple denoting the position of the right button. The left button will be symmetric.
        #: - A list with (x,y) positions of both buttons - [(xleft,yleft), (xright,yright)]
        self.resp_btn_positions = resp_btn_positions

        #: Colour of the response button. If two colours are provided, they will be used
        #: for the left and right buttons, correspondingly.
        self.resp_btn_colours = resp_btn_colours

        #: Text of the response buttons. If two texts are provided, they will be used
        #: for the left and right buttons, correspondingly.
        self.resp_btn_texts = resp_btn_texts


        #: Font name (relevant only when resp_btn_texts is provided)
        self.resp_btn_font_name = resp_btn_font_name

        #: Font size (relevant only when resp_btn_texts is provided)
        self.resp_btn_font_size = resp_btn_font_size

        #: Font color (relevant only when resp_btn_texts is provided)
        self.resp_btn_text_colour = resp_btn_text_colour


        #----- Configuration of visual feedback -----

        #: The kind of feedback stimulus to show, following a participant response:
        #: 'rectangle', 'picture', or None
        self.feedback_stim_type = feedback_stim_type

        #: Where to place the feedback stimuli. This affects the default values of
        #: :attr:`~trajtrackerp.dchoice.Config.feedback_stim_position` and
        #: :attr:`~trajtrackerp.dchoice.Config.feedback_btn_colours`
        #:
        #: Valid values:
        #:
        #: - 'buttons': over the response buttons
        #: - 'middle': between the buttons (on top of screen)
        self.feedback_place = feedback_place

        #: The size of the feedback stimuli (optional): either (width, height) if both have the same size,
        #: or an array of two sizes i.e. [(width1, height1), (width2, height2)].
        #:
        #: - For feedback_place = 'button', the default size is the size of the response buttons.
        #: - For feedback_place = 'middle', you should either specify feedback_rect_size and
        #:   feedback_stim_position or neither of them.
        #:   Default: the feedback rectangle will be at the top of the screen, between the two buttons.
        #:
        #:   For feedback_place = 'middle', if a single number is defined here, it denotes
        #:   the rectangle's height.
        self.feedback_rect_size = feedback_rect_size

        #: The position of the feedback stimulus (optional) - either (x,y) coordinates (indicating that
        #: both feedback areas are in the same location) or [(x1,y1), (x2,y2)].
        #:
        #: - For feedback_place = 'middle', the default position is in the middle-top of the screen.
        #: - For feedback_place = 'button', the default position is at the two top corners of the screen.
        self.feedback_stim_position = feedback_stim_position

        #: How to determine which feedback to show.
        #:
        #: - *'response'*: The feedback is determined by the button touched
        #: - *'expected'*: The feedback is the button that should be pressed
        #: - *'accuracy'*: The feedback is determined by whether the touched button was correct.
        #:                 (when configuring the two feedback stimuli, e.g., size and position,
        #:                 the first one refers to correct response).
        #:                 If you use this feature, you must include an "expected_response" column in the
        #:                 trials CSV file.
        self.feedback_select_by = feedback_select_by

        #: The colour of the feedback button/rectangle. If two colors are provided, the first colour will
        #: be used for correct responses and the second colour for incorrect responses
        self.feedback_btn_colours = feedback_btn_colours

        #: Duration (in seconds) for which feedback is presented
        self.feedback_duration = feedback_duration

        #: Pictures to use as feedback (when feedback_mode = 'picture').
        #: Specify here two expyriment.stimuli.Picture objects.
        self.feedback_pictures = feedback_pictures

        self.confidence_slider_height = 0.8
        self.confidence_slider_y = 0
