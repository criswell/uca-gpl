# Unified Client Agent Release Builder Helper
# -------------------------------------------
# Contains helper functions and dependencies for the release builder.

###########################################################
# Convenience defintions for the various bash color prompts
###########################################################
COLOR_RESET='\e[0m'
COLOR_TRACE='\e[0;34m' # Blue
COLOR_WARNING='\e[1;33m' # Yellow
COLOR_ALERT='\e[4;31m' # Underline red
COLOR_DIE='\e[30m\033[41m' # Red background, black text

#################
# Trace functions
#################
inner_trace () {
    if [ -n "$LOG_FILE" ]; then
        echo -e "$(date) $*" >> ${LOG_FILE}
    else
        echo -e "$*"
    fi
}

warning () {
    if [ -n "$LOG_FILE" ]; then
        inner_trace "$*"
    else
        inner_trace "${COLOR_WARNING}$*${COLOR_RESET}"
    fi
}

trace () {
    if [ -n "$LOG_FILE" ]; then
        inner_trace "$*"
    else
        inner_trace "${COLOR_TRACE}$*${COLOR_RESET}"
    fi
}

alert() {
    if [ -n "$LOG_FILE" ]; then
        inner_trace "$*"
    else
        inner_trace "${COLOR_ALERT}$*${COLOR_RESET}"
    fi
}

die() {
    if [ -n "$LOG_FILE" ]; then
        inner_trace "$*"
    else
        inner_trace "${COLOR_DIE}$*${COLOR_RESET}"
    fi
    cleanup_env
    exit 1
}

# vim:set ai et sts=4 sw=4 tw=80: