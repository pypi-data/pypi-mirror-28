"""
Functions to support the discrete-decision paradigm

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

import trajtracker as ttrk
import trajtracker.utils as u
from trajtracker.validators import ExperimentError
from trajtrackerp import common
from trajtrackerp.common import RunTrialResult, FINGER_LIFTED

from trajtrackerp.dchoice import TrialInfo, hide_feedback_stimuli


#----------------------------------------------------------------
def run_trials(exp_info):
    return common.run_trials(exp_info, run_trial, TrialInfo)


#----------------------------------------------------------------
def run_trial(exp_info, trial, trial_already_initiated):
    """
    Run a single trial

    :param exp_info:
    :type exp_info: trajtracker.paradigms.dchoice.ExperimentInfo
    
    :param trial:
    :type trial: trajtracker.paradigms.dchoice.TrialInfo
    
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

    hide_feedback_stimuli(exp_info)
    common.on_finger_touched_screen(exp_info, trial)

    rc = common.wait_until_finger_moves(exp_info, trial)
    if rc is not None:
        if rc[1] is not None:
            trial_failed(rc[1], exp_info, trial)
        return rc[0]

    time_response_made = None

    while True:  # This loop runs once per frame

        curr_time = u.get_time()

        #-- Inform relevant objects (validators, trajectory tracker, event manager, etc.) of the progress
        err = common.update_movement_in_traj_sensitive_objects(exp_info, trial)
        if err is not None:
            trial_failed(err, exp_info, trial)
            return RunTrialResult.Failed

        #-- Check if a response button was reached
        user_response = get_touched_button(exp_info)
        if user_response is not None and time_response_made is None:

            time_response_made = curr_time
            common.on_response_made(exp_info, trial, curr_time)

            min_movement_time = trial.csv_data['min_movement_time'] if ('min_movement_time' in trial.csv_data) else exp_info.config.min_movement_time
            if trial.movement_time < min_movement_time:
                trial_failed(ExperimentError(ttrk.validators.InstantaneousSpeedValidator.err_too_fast,
                                             "Please move more slowly"),
                             exp_info, trial)
                return RunTrialResult.Failed

            exp_info.sounds_ok[0].play()
            trial.stopped_moving_event_dispatched = True

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
        trial_succeeded(exp_info, trial, user_response)

    return run_trial_result


#----------------------------------------------------------------
def get_touched_button(exp_info):
    """
    Check if any response button was touched

    :type exp_info: trajtracker.paradigms.dchoice.ExperimentInfo 

    :return: The number of the touched button, or None if no button was touched
    """

    for hotspot in exp_info.response_hotspots:
        if hotspot.touched:
            return hotspot.button_number

    return None


#----------------------------------------------------------------
def initialize_trial(exp_info, trial):
    """
    Initialize a trial

    :type exp_info: trajtracker.paradigms.dchoice.ExperimentInfo 
    :type trial: trajtracker.paradigms.dchoice.TrialInfo 
    """

    exp_info.start_point.reset()
    for hotspot in exp_info.response_hotspots:
        hotspot.reset()

    #-- Reset the display for this trial
    exp_info.stimuli.present()

    common.update_text_target_for_trial(exp_info, trial)
    common.update_generic_target_for_trial(exp_info, trial)
    if exp_info.fixation is not None:
        common.update_fixation_for_trial(exp_info, trial)

    exp_info.event_manager.dispatch_event(ttrk.events.TRIAL_INITIALIZED, 0, u.get_time() - exp_info.session_start_time)

    # -- Update the display to present stuff that may have been added by the TRIAL_INITIALIZED event listeners
    exp_info.stimuli.present()

    if exp_info.config.stimulus_then_move:
        trial.targets_t0 = u.get_time() - trial.start_time


#----------------------------------------------------------------
def trial_failed(err, exp_info, trial):
    """
    Called when the trial failed for any reason 
    (only when a strict error occurred; pointing at an incorrect location does not count as failure) 

    :param err: The error that occurred
    :type err: ExperimentError
    :param exp_info:
    :type exp_info: trajtracker.paradigms.dchoice.ExperimentInfo
    :param trial:
    :type trial: trajtracker.paradigms.dchoice.TrialInfo
    """
    common.trial_failed_common(err, exp_info, trial)
    trial_ended(exp_info, trial, "ERR_" + err.err_code, -1)


#----------------------------------------------------------------
def trial_succeeded(exp_info, trial, user_response):
    """
    Called when the trial ends successfully (this does not mean that the answer was correct) 
    
    :param exp_info:
    :type exp_info: trajtracker.paradigms.dchoice.ExperimentInfo
    :param trial:
    :type trial: trajtracker.paradigms.dchoice.TrialInfo
    :param user_response: The button selected by the user (0=left, 1=right) 
    """

    common.trial_succeeded_common(exp_info, trial)

    show_feedback(exp_info, trial, user_response)

    trial_ended(exp_info, trial, "OK", user_response)

    exp_info.trajtracker.save_to_file(trial.trial_num)


#------------------------------------------------
def show_feedback(exp_info, trial, user_response):
    """
    Show the feedback stimulus  

    :param exp_info:
    :type exp_info: trajtracker.paradigms.dchoice.ExperimentInfo
    :param trial:
    :type trial: trajtracker.paradigms.dchoice.TrialInfo
    :param user_response: The button selected by the user (0=left, 1=right) 
    """

    fb_ind = get_feedback_stim_num(exp_info, trial, user_response)
    exp_info.feedback_stimuli[fb_ind].visible = True


#------------------------------------------------
def get_feedback_stim_num(exp_info, trial, user_response):
    """
    Return the number of the feedback stimulus to show (0 or 1)  

    :param exp_info:
    :type exp_info: trajtracker.paradigms.dchoice.ExperimentInfo
    :param trial:
    :type trial: trajtracker.paradigms.dchoice.TrialInfo
    :param user_response: The button selected by the user (0=left, 1=right) 
    """

    selectby = exp_info.config.feedback_select_by

    if selectby == 'accuracy':
        correct = trial.expected_response == user_response
        return 1 - correct

    elif selectby == 'response':
        return user_response

    elif selectby == 'expected':
        return trial.expected_response

    else:
        raise ttrk.ValueError("Unsupported config.feedback_select_by ({:})".format(selectby))


#------------------------------------------------
def trial_ended(exp_info, trial, success_err_code, user_response):
    """
    This function is called whenever a trial ends, either successfully or with failure.
    It updates the result files.

    :type exp_info: trajtracker.paradigms.dchoice.ExperimentInfo 
    :type trial: trajtracker.paradigms.dchoice.TrialInfo 
    :param success_err_code: A string code to write as status for this trial
    :param user_response: The number of the button that was pressed (-1 = no button)
    """

    exp_info.stimuli.present()

    if exp_info.config.save_results:
        update_trials_file(exp_info, trial, success_err_code, user_response)

        #-- Save the session at the end of each trial, to make sure it's always saved - even if
        #-- the experiment software unexpectedly terminates
        common.save_session_file(exp_info, "DC")


#------------------------------------------------
def update_trials_file(exp_info, trial, success_err_code, user_response):
    """
    Add an entry (line) to the trials.csv file

    :type exp_info: trajtracker.paradigms.dchoice.ExperimentInfo 
    :type trial: trajtracker.paradigms.dchoice.TrialInfo 
    :param success_err_code: A string code to write as status for this trial 
    :param user_response: The number of the button that was pressed (-1 = no button)
    """

    trial_out_row = common.prepare_trial_out_row(exp_info, trial, success_err_code)

    trial_out_row['expectedResponse'] = -1 if trial.expected_response is None else trial.expected_response
    trial_out_row['UserResponse'] = user_response

    if exp_info.trials_file_writer is None:
        common.open_trials_file(exp_info, ['expectedResponse', 'UserResponse'])

    exp_info.trials_file_writer.writerow(trial_out_row)
    exp_info.trials_out_fp.flush()

