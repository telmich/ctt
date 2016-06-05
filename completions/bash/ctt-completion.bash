_ctt()
{
    local cur prev opts cmds projects
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="-h --help -d --debug -v --verbose"
    cmds="listprojects track report"

    case "${prev}" in
        track|report)
            if [[ -d ~/.ctt ]]; then
                projects=$(ls ~/.ctt)
            else
                projects=""
            fi
            ;;
    esac

    case "${prev}" in
        -*|listprojects)
            COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
            return 0
            ;;
        track)
            opts="-h --help -d --debug -v --verbose --sd --start --ed --end -n --no-comment"
            COMPREPLY=( $(compgen -W "${opts} ${projects}" -- ${cur}) )
            return 0
            ;;
        report)
            opts="-h --help -d --debug -v --verbose --sd --start --ed --end -a --all -e --regexp -i --ignore-case -f -format -s --summary"
            COMPREPLY=( $(compgen -W "${opts} ${projects}" -- ${cur}) )
            return 0
            ;;
        *)
            ;;
    esac

    if [[ ${cur} == -* ]]; then 
    	COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
    	return 0
    fi

    COMPREPLY=( $(compgen -W "${cmds}" -- ${cur}) )
    return 0
}

complete -F _ctt ctt
