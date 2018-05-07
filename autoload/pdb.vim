hi def link Breakpoint Error
sign define breakpoint linehl=Breakpoint  text=xx
hi def link CurrentLine DiffAdd
sign define current_line linehl=CurrentLine text=>>

pyx import pdb_debug
pyx pipe = None

fun! s:escape_path()
    return substitute(expand('%:p'), '\', '\\\\', 'g')
endfunction

fun! s:enable_startup()
    return pyxeval('pipe is not None')
endfunction

fun! pdb#quit() abort
		sign unplace *
		pyx del pipe
		pyx pipe = None
endfunction

fun! pdb#toggle() abort
    if !s:enable_startup()
        exe "pyx pipe = pdb_debug.PdbDebug('".s:escape_path()."')"
    else
        call pdb#quit()
    endif
endfunction

fun! pdb#breakpoint() abort
    if !s:enable_startup() | return | endif
    let lines = pyxeval("pipe.breakpoint('".s:escape_path()."',".line('.').")")
    if lines[0] != "" && lines[1] > 0
        exe ":sign place 110 line=".lines[1]." name=breakpoint file=".lines[0]
    elseif lines[1] == -1
        exe ":sign unplace"
    endif
endfunction

fun! pdb#run(op) abort
    if !s:enable_startup() | return | endif
    let lines = pyxeval('pipe.step('.a:op.')')
    if lines[0] != "" && lines[1] > 0
        if get(lines, 2, "") != ""
            exec ":echohl WarningMsg | echom '".lines[2]."' | echohl None"
        endif
        
        sign unplace 111
        exe ":drop ".lines[0]." | normal ".lines[1]."G | normal zz"
        exe ":sign place 111 line=".lines[1]." name=current_line file=" . lines[0]
    else
				call pdb#exit()
    endif
endfunction

fun! pdb#print(word)
    if (!s:enable_startup() || a:word == '') | return | endif

    let line = pyxeval('pipe.pprint("'.a:word.'")')
    echom line
endfunction