hi def link Breakpoint Error
sign define breakpoint linehl=Breakpoint  text=xx
hi def link CurrentLine DiffAdd
sign define current_line linehl=CurrentLine text=>>

pyx import pdbpipe
pyx pipe = None

fun! s:escape_path()
    return substitute(expand('%:p'), '\', '\\\\', 'g')
endfunction

fun! s:enable_startup()
    return pyxeval('pipe is not None')
endfunction

fun! pdbpipe#startup() abort
    if !s:enable_startup()
        exe "pyx pipe = pdbpipe.Pdbpipe('".s:escape_path()."')"
    endif
endfunction

fun! pdbpipe#quit() "{{{
    sign unplace *
    pyx del pipe
    pyx pipe = None
endfunction "}}}

fun! pdbpipe#next() abort
    call pdbpipe#run('next')
endfunction

fun! pdbpipe#continue() abort
    call pdbpipe#run('continues')
endfunction

fun! pdbpipe#breakpoint() abort
    if !s:enable_startup() | return | endif
    let lines = pyxeval("pipe.breakpoint('".s:escape_path()."',".line('.').")")
    if lines[0] != "" && lines[1] != 0
        exe ":sign place 110 line=".lines[1]." name=breakpoint file=".lines[0]
    elseif lines[1] == -1
        exe ":sign unplace"
    endif
endfunction

fun! pdbpipe#step() abort
    call pdbpipe#run('step')
endfunction

fun! pdbpipe#run(op) abort
    if !s:enable_startup() | return | endif
    let lines = pyxeval('pipe.'.a:op.'()')
    if lines[0] != "" && lines[1] != 0
        sign unplace 111
        exe ":drop ".lines[0]
        exe ":normal ".lines[1]."G"
        exe ":normal zz"
        exe ":sign place 111 line=".lines[1]." name=current_line file=" . lines[0]
    else
        call pdbpipe#quit()
    endif
endfunction
