# Command dispatcher

# INTERNAL RUN COMMAND
# Not intended to be used externally
_run_command() {
    # FIXME Do we want to do any error checking here?
    # Currently fire and forget
    #${BIN_DIR}/elevate_script ${SCRIPTS_DIR}/${PLATFORM_NAME}_${*}
    # FIXME - We need to solve the script elevate problems!
    ${SCRIPTS_DIR}/${PLATFORM_NAME}_${*}

    echo $?
}

# This is the general command processor.
#
# Its job is to take the incoming commands from the client agent
# directory, interpret what they mean, and then dispatch them to the
# various bit players around the Linux box which ultimately perform
# those actions we need done (rebooting, diagnosing network errors, etc.)
process_command() {
    if [ "$*" = "reboot" ]; then
        _run_command "reboot"
    elif [ "$*" = "tcp_diag" ]; then
        _run_command "tcp_diag"
    elif [ "$*" = "asset_refresh" ]; then
        _run_command "asset_refresh"
    elif [ "$*" = "client_update" ]; then
        _run_command "client_update"
    elif [ "$*" = "asset_done_reboot" ]; then
        _run_command "asset_done_reboot"
    fi
}
