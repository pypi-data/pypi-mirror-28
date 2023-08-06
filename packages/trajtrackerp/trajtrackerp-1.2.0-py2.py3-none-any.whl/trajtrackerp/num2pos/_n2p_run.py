"""
Functions to support the number-to-position paradigm

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

from __future__ import division

import expyriment as xpy
import numpy as np

import trajtracker as ttrk
import trajtracker.utils as u
from trajtrackerp import common
from trajtrackerp.common import RunTrialResult, FINGER_LIFTED
from trajtracker.validators import ExperimentError

from trajtrackerp.num2pos import TrialInfo


#----------------------------------------------------------------
def run_trials(exp_info):
    return common.run_trials(exp_info, run_trial, TrialInfo)


#----------------------------------------------------------------
def run_trial(exp_info, trial, trial_already_initiated):
    """
    Run a single trial
    
    :type exp_info: trajtracker.paradigms.num2pos.ExperimentInfo 
    :type trial: trajtracker.paradigms.num2pos.TrialInfo
    :param trial_already_initiated: Indicates if the "start" point was already touched
    
    :return: RunTrialResult
    """

    config = exp_info.config

    initialize_trial(exp_info, trial)

    if trial_already_initiated:
        exp_info.start_point.mark_as_initialized()

    else:
        exp_info.start_point.wait_until_startpoint_touched(exp_info.xpy_exp,
                                                           on_loop_present=exp_info.stimuli,
                                                           event_manager=exp_info.event_manager,
                                                           trial_start_time=trial.start_time,
                                                           session_start_time=exp_info.session_start_time)
    on_finger_touched_screen(exp_info, trial)

    rc = common.wait_until_finger_moves(exp_info, trial)
    if rc is not None:
        if rc[1] is not None:
            trial_failed(rc[1], exp_info, trial)
        return rc[0]

    nl = exp_info.numberline
    time_response_made = None

    while True:  # This loop runs once per frame

        curr_time = u.get_time()

        #-- Inform relevant objects (validators, trajectory tracker, event manager, etc.) of the progress
        err = common.update_movement_in_traj_sensitive_objects(exp_info, trial)
        if err is not None:
            trial_failed(err, exp_info, trial)
            return RunTrialResult.Failed

        #-- Check if the number line was reached
        if nl.touched and time_response_made is None:

            time_response_made = curr_time
            common.on_response_made(exp_info, trial, curr_time)

            #-- Validate that the response wasn't too far off the number line's ends
            max_excess = exp_info.config.max_response_excess
            if max_excess is not None and (nl.response_value < nl.min_value or nl.response_value > nl.max_value):
                excess = (nl.min_value - nl.response_value) if (nl.response_value < nl.min_value) \
                    else (nl.response_value - nl.max_value)
                excess /= (nl.max_value - nl.min_value)
                if excess > max_excess:
                    trial_failed(ExperimentError("ResponseTooFar", "Please point at the number line"),
                                 exp_info, trial)
                    return RunTrialResult.Failed

            #-- Validate that the response wasn't too fast
            min_movement_time = trial.csv_data['min_movement_time'] if ('min_movement_time' in trial.csv_data) else exp_info.config.min_movement_time
            if trial.movement_time < min_movement_time:
                trial_failed(ExperimentError(ttrk.validators.InstantaneousSpeedValidator.err_too_fast,
                                             "Please move more slowly"),
                             exp_info, trial)
                return RunTrialResult.Failed

            play_success_sound(exp_info, trial)

            if exp_info.config.post_response_target:
                exp_info.numberline.show_target_pointer_on(trial.target)

        #-- Successful end-of-trial conditions
        if time_response_made is not None:

            time_in_trial = curr_time - trial.start_time

            if not ttrk.env.mouse.check_button_pressed(0):
                #-- Finger was lifted
                trial.time_finger_lifted = time_in_trial
                exp_info.event_manager.dispatch_event(FINGER_LIFTED, time_in_trial,
                                                      curr_time - exp_info.session_start_time)
                break

            if curr_time > time_response_made + config.max_post_response_record_duration:
                #-- post-response duration has expired
                break

        xpy.io.Keyboard.process_control_keys()

        #-- Update all displayable elements.
        #-- This is done when the loop ends, not when it starts, because there was another present()
        #-- call just before the loop, inside wait_until_finger_moves()
        exp_info.stimuli.present()

    #-- Main task ended successfully

    #-- Optionally, run additional stages
    run_trial_result = common.run_post_trial_operations(exp_info, trial)
    if run_trial_result in (RunTrialResult.Succeeded, RunTrialResult.SucceededAndProceed):
        trial_succeeded(exp_info, trial)

    return run_trial_result


#----------------------------------------------------------------
def on_finger_touched_screen(exp_info, trial):
    """
    This function should be called when the finger touches the screen

    :type exp_info: trajtracker.paradigms.num2pos.ExperimentInfo
    :type trial: trajtracker.paradigms.num2pos.TrialInfo
    """

    update_numberline_for_trial(exp_info, trial)
    common.on_finger_touched_screen(exp_info, trial)


#----------------------------------------------------------------
def initialize_trial(exp_info, trial):
    """
    Initialize a trial
    
    :type exp_info: trajtracker.paradigms.num2pos.ExperimentInfo 
    :type trial: trajtracker.paradigms.num2pos.TrialInfo 
    """

    exp_info.start_point.reset()
    exp_info.numberline.reset()    # mark the line as yet-untouched

    exp_info.stimuli.present()  # reset the display

    common.update_text_target_for_trial(exp_info, trial, use_numeric_target_as_default=True)
    common.update_generic_target_for_trial(exp_info, trial)
    if exp_info.fixation is not None:
        common.update_fixation_for_trial(exp_info, trial)

    exp_info.numberline.target = trial.target

    exp_info.event_manager.dispatch_event(ttrk.events.TRIAL_INITIALIZED, 0, u.get_time() - exp_info.session_start_time)

    #-- Update the display to present stuff that may have been added by the TRIAL_INITIALIZED event listeners
    exp_info.stimuli.present()

    if exp_info.config.stimulus_then_move:
        trial.targets_t0 = u.get_time() - trial.start_time


#------------------------------------------------
def update_numberline_for_trial(exp_info, trial):
    """
    Update the number line when the trial is initialized

    :type exp_info: trajtracker.paradigms.num2pos.ExperimentInfo
    :type trial: trajtracker.paradigms.num2pos.TrialInfo
    """

    upd_xy = common.update_attr_by_csv_config(exp_info, trial, exp_info.numberline, 'nl.position', 'position')

    upd_x = common.update_obj_position(exp_info, trial, exp_info.numberline, 'nl', 'x')
    upd_y = common.update_obj_position(exp_info, trial, exp_info.numberline, 'nl', 'y')

    #-- Save number line coordinates in output file

    if upd_xy or upd_x:
        exp_info.exported_trial_result_fields['nl.position.x'] = None
        trial.results['nl.position.x'] = exp_info.numberline.position[0]

    if upd_xy or upd_y:
        exp_info.exported_trial_result_fields['nl.position.y'] = None
        trial.results['nl.position.y'] = exp_info.numberline.position[1]


#------------------------------------------------
# This function is called when a trial ends with an error
#
def trial_failed(err, exp_info, trial):
    """
    Called when the trial failed for any reason 
    (only when a strict error occurred; pointing at an incorrect location does not count as failure) 

    :type err: ExperimentError
    :type exp_info: trajtracker.paradigms.num2pos.ExperimentInfo
    :type trial: trajtracker.paradigms.num2pos.TrialInfo 
    """
    common.trial_failed_common(err, exp_info, trial)
    trial_ended(exp_info, trial, "ERR_" + err.err_code)


#------------------------------------------------
# This function is called when a trial ends with no error
#
def trial_succeeded(exp_info, trial):
    """
    Called when the trial ends successfully (i.e. the finger touched the numberline - doesn't matter where)
    
    :type exp_info: trajtracker.paradigms.num2pos.ExperimentInfo
    :type trial: trajtracker.paradigms.num2pos.TrialInfo 
    """

    common.trial_succeeded_common(exp_info, trial)
    trial_ended(exp_info, trial, "OK")
    exp_info.trajtracker.save_to_file(trial.trial_num)


#------------------------------------------------
def trial_ended(exp_info, trial, success_err_code):
    """
    This function is called whenever a trial ends, either successfully or with failure.
    It updates the result files.
    
    :type exp_info: trajtracker.paradigms.num2pos.ExperimentInfo 
    :type trial: trajtracker.paradigms.num2pos.TrialInfo 
    :param success_err_code: A string code to write as status for this trial 
    """

    exp_info.stimuli.present()

    if exp_info.config.save_results:
        update_trials_file(exp_info, trial, success_err_code)

        #-- Save the session at the end of each trial, to make sure it's always saved - even if
        #-- the experiment software unexpectedly terminates
        common.save_session_file(exp_info, "NL")


#------------------------------------------------
def update_trials_file(exp_info, trial, success_err_code):
    """
    Add an entry (line) to the trials.csv file
    
    :type exp_info: trajtracker.paradigms.num2pos.ExperimentInfo 
    :type trial: trajtracker.paradigms.num2pos.TrialInfo 
    :param success_err_code: A string code to write as status for this trial 
    """

    trial_out_row = common.prepare_trial_out_row(exp_info, trial, success_err_code)

    endpoint = exp_info.numberline.response_value
    trial_out_row['endPoint'] = "N/A" if endpoint is None else "{:.3g}".format(endpoint)
    trial_out_row['target'] = trial.target

    if exp_info.trials_file_writer is None:
        common.open_trials_file(exp_info, ['target', 'endPoint'])

    exp_info.trials_file_writer.writerow(trial_out_row)
    exp_info.trials_out_fp.flush()


#------------------------------------------------
def play_success_sound(exp_info, trial):
    """
    Play a "trial succeeded" sound. If required in the configuration, we select here the sound
    depending on the endpoint error.

    :type exp_info: trajtracker.paradigms.num2pos.ExperimentInfo
    :type trial: trajtracker.paradigms.num2pos.TrialInfo 
    """

    endpoint_err = np.abs(exp_info.numberline.response_value - trial.target)
    endpoint_err_ratio = min(1, endpoint_err / (exp_info.numberline.max_value - exp_info.numberline.min_value))
    sound_ind = np.where(endpoint_err_ratio <= exp_info.sounds_ok_max_ep_err)[0][0]
    exp_info.sounds_ok[sound_ind].play()

