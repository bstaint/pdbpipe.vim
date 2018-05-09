hi def link Breakpoint Todo
sign define breakpoint linehl=Breakpoint  text=xx
hi def link CurrentLine DiffAdd
sign define current_line linehl=CurrentLine text=>>

pyx import pdb_debug
pyx pipe = None

let s:signid = 120
let s:breakpoints = []

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
        let s:signid = 120
        let s:breakpoints = []
    else
        call pdb#quit()
    endif
endfunction

fun! pdb#breakpoint() abort
    if !s:enable_startup() | return | endif
    let lines = pyxeval("pipe.breakpoint('".s:escape_path()."',".line('.').")")
    if lines[1] > 0
        silent exe ":sign place ".s:signid." line=".lines[1]." name=breakpoint file=".lines[0]
        call add(s:breakpoints, s:signid)
        let s:signid += 1        
    else
        let id = remove(s:breakpoints, abs(lines[1]))
        silent exe ":sign unplace ".id." file=".lines[0]
    endif
endfunction

fun! pdb#run(op) abort
    if !s:enable_startup() | return | endif
    let lines = pyxeval('pipe.step('.a:op.')')
    if get(lines, 2, "") != ""
        exec ":redraws! | echohl ErrorMsg | echom '".lines[2]."' | echohl None"
    endif
        
    if lines[0] != "" && lines[1] > 0
        sign unplace 111
        silent exec ":drop ".lines[0]." | normal ".lines[1]."G"
        silent exec 'normal! zz'
        exe ":sign place 111 line=".lines[1]." name=current_line file=" . lines[0]
    else
        call pdb#quit()
    endif
endfunction

fun! pdb#print(word)
    if (!s:enable_startup() || a:word == '') | return | endif
    let word = substitute(a:word, '"', '\\"', 'g')
    let line = pyxeval('pipe.pprint("'.l:word.'")')
    echom line
endfunction
