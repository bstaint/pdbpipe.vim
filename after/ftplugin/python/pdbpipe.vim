nnoremap <silent> <Plug>PdbStartup :call pdbpipe#startup()<CR>
nnoremap <silent> <Plug>PdbBP :call pdbpipe#breakpoint()<CR>
nnoremap <silent> <Plug>PdbNext :call pdbpipe#next()<CR>
nnoremap <silent> <Plug>PdbStep :call pdbpipe#step()<CR>
nnoremap <silent> <Plug>PdbQuit :call pdbpipe#quit()<CR>
nnoremap <silent> <Plug>PdbRun :call pdbpipe#continue()<CR>

nnoremap [pdbpipe] <Nop>
nmap <Leader>d [pdbpipe]
if !hasmapto('<Plug>PdbStartup', 'n')
	nmap <unique> [pdbpipe]t <Plug>PdbStartup
endif

if !hasmapto('<Plug>PdbBP', 'n')
	nmap <unique> [pdbpipe]b <Plug>PdbBP
endif

if !hasmapto('<Plug>PdbRun', 'n')
	nmap <unique> [pdbpipe]r <Plug>PdbRun
endif

if !hasmapto('<Plug>PdbQuit', 'n')
	nmap <unique> [pdbpipe]q <Plug>PdbQuit
endif

if !hasmapto('<Plug>PdbStep', 'n')
	nmap <unique> [pdbpipe]s <Plug>PdbStep
endif

if !hasmapto('<Plug>PdbNext', 'n')
	nmap <unique> [pdbpipe]n <Plug>PdbNext
endif