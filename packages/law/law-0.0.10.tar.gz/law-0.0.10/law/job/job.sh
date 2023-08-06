#!/usr/bin/env bash

# generic law job script

# render variables:
# - log_file: a file for logging stdout and stderr simultaneously
# - input_files: basenames of all input files
# - bootstrap_file: file that is sourced before running tasks
# - stageout_file: file that is executed after running tasks
# - dashboard_file: file that contains dashboard functions to be used in hooks

# arguments:
# 1. task_module
# 2. task_family
# 3. task_params (base64 encoded)
# 4. start_branch
# 5. end_branch
# 6. auto_retry
# 7. dashboard_data (base64 encoded)

action() {
    local origin="$( /bin/pwd )"


    #
    # store arguments
    #

    local task_module="$1"
    local task_family="$2"
    local task_params="$( echo "$3" | base64 --decode )"
    local start_branch="$4"
    local end_branch="$5"
    local auto_retry="$6"
    local dashboard_data="$( echo "$7" | base64 --decode )"


    #
    # create a new home and tmp dirs, and change into the new home dir and copy all input files
    #

    local ret="0"
    local job_hash="$( python -c "import uuid; print(str(uuid.uuid4())[-12:])" )"
    export HOME="$origin/job_${job_hash}"
    export TMP="$HOME/tmp"
    export TEMP="$TMP"
    export TMPDIR="$TMP"
    export LAW_TARGET_TMP_DIR="$TMP"

    mkdir -p "$HOME"
    mkdir -p "$TMP"

    if [ ! -z "{{input_files}}" ]; then
        cp {{input_files}} "$HOME/"
    fi

    cd "$HOME"


    #
    # helper functions
    #

    line() {
        local n="${1-80}"
        local c="${2--}"
        local l=""
        for (( i=0; i<$n; i++ )); do
            l="$l$c"
        done
        echo "$l"
    }

    section() {
        local title="$@"
        local length="${#title}"

        echo
        if [ "$length" = "0" ]; then
            line 80
        else
            local rest="$( expr 80 - 4 - $length )"
            echo "$( line 2 ) $title $( line $rest )"
        fi
    }

    cleanup() {
        section cleanup

        cd "$origin"

        echo "pre cleanup"
        echo "ls -la $HOME:"
        ls -la "$HOME"
        rm -rf "$HOME"
        echo
        echo "post cleanup"
        echo "ls -la $origin:"
        ls -la "$origin"
    }

    call_func() {
        local name="$1"
        local args="${@:2}"

        # function existing?
        type -t "$name" &> /dev/null
        if [ "$?" = "0" ]; then
            $name "$@"
        fi
    }

    call_hook() {
        section "hook '$1'"
        call_func "$@"
        section
    }


    #
    # some logs
    #

    section environment

    echo "script: $0"
    echo "shell : '$SHELL'"
    echo "args  : '$@'"
    echo "origin: '$origin'"
    echo "home  : '$HOME'"
    echo "tmp   : '$( python -c "from tempfile import gettempdir; print(gettempdir())" )'"
    echo "pwd   : '$( pwd )'"
    echo
    echo "task module   : $task_module"
    echo "task family   : $task_family"
    echo "task params   : $task_params"
    echo "start branch  : $start_branch"
    echo "end branch    : $end_branch"
    echo "auto retry    : $auto_retry"
    echo "dashboard data: $dashboard_data"
    echo
    echo "ls -la:"
    ls -la


    #
    # dashboard file
    #

    load_dashboard_file() {
        local dashboard_file="{{dashboard_file}}"
        if [ ! -z "$dashboard_file" ]; then
            echo "load dashboard file $dashboard_file"
            source "$dashboard_file"
        else
            echo "dashboard file empty, skip"
        fi
    }

    section "dashboard file"

    load_dashboard_file

    if [ "$?" != "0" ]; then
        2>&1 echo "dashboard file failed"
    fi


    #
    # custom bootstrap file
    #

    run_bootstrap_file() {
        local bootstrap_file="{{bootstrap_file}}"
        if [ ! -z "$bootstrap_file" ]; then
            echo "run bootstrap file $bootstrap_file"
            source "$bootstrap_file"
        else
            echo "bootstrap file empty, skip"
        fi
    }

    section "bootstrap file"

    run_bootstrap_file
    ret="$?"

    if [ "$ret" != "0" ]; then
        2>&1 echo "bootstrap file failed, abort"
        cleanup
        return "$ret"
    fi


    #
    # detect law
    #

    section "detect law"

    export LAW_SRC_PATH="$( python -c "import os, law; print('RESULT:' + os.path.dirname(law.__file__))" | grep -Po "RESULT:\K([^\s]+)" )"

    if [ -z "$LAW_SRC_PATH" ]; then
        2>&1 echo "law not found (should be loaded in bootstrap file), abort"
        cleanup
        return "1"
    fi

    echo "found law at $LAW_SRC_PATH"


    #
    # run the law task commands
    #

    call_hook law_hook_job_running

    for (( branch=$start_branch; branch<$end_branch; branch++ )); do
        section "branch $branch"

        local cmd="law run $task_module.$task_family --branch $branch $task_params"
        echo "cmd: $cmd"

        echo

        echo "dependecy tree:"
        eval "$cmd --print-deps 2"
        ret="$?"
        if [ "$?" != "0" ]; then
            2>&1 echo "dependency tree for branch $branch failed, abort"
            call_hook law_hook_job_failed "$ret"
            cleanup
            return "$ret"
        fi

        echo

        echo "execute attempt 1:"
        eval "$cmd"
        ret="$?"
        echo "return code: $ret"

        if [ "$ret" != "0" ] && [ "$auto_retry" = "yes" ]; then
            echo

            echo "execute attempt 2:"
            eval "$cmd"
            ret="$?"
            echo "return code: $ret"
        fi

        if [ "$ret" != "0" ]; then
            2>&1 echo "branch $branch failed with exit code $ret, abort"
            call_hook law_hook_job_failed "$ret"
            cleanup
            return "$ret"
        fi
    done


    #
    # custom stageout file
    #

    run_stageout_file() {
        local stageout_file="{{stageout_file}}"
        if [ ! -z "$stageout_file" ]; then
            echo "run stageout file $stageout_file"
            bash "$stageout_file"
        else
            echo "stageout file empty, skip"
        fi
    }

    section stageout

    run_stageout_file
    ret="$?"

    if [ "$ret" != "0" ]; then
        2>&1 echo "stageout file failed, abort"
        call_hook law_hook_job_failed "$ret"
        cleanup
        return "$ret"
    fi


    #
    # le fin
    #

    call_hook law_hook_job_finished
    cleanup

    return "0"
}

# start and optionally log
if [ -z "{{log_file}}" ]; then
    action "$@"
else
    action "$@" &>> "{{log_file}}"
fi
