nnoremap <silent> <Plug>PdbStartup :call pdbpipe#startup()<CR>
nnoremap <silent> <Plug>PdbBP :call pdbpipe#breakpoint()<CR>
nnoremap <silent> <Plug>PdbNext :call pdbpipe#next()<CR>
nnoremap <silent> <Plug>PdbStep :call pdbpipe#step()<CR>
nnoremap <silent> <Plug>PdbQuit :call pdbpipe#quit()<CR>
nnoremap <silent> <Plug>PdbRun :call pdbpipe#continue()<CR>
nnoremap <silent> <Plug>PdbPrintCword :call pdbpipe#print(expand('<cword>'))<CR>

if !hasmapto('<Plug>PdbPrintCword', 'n')
	nmap <unique> <Leader>p <Plug>PdbPrintCword
endif

if !hasmapto('<Plug>PdbRun', 'n')
	nmap <unique> <Leader>5 <Plug>PdbRun
endif

if !hasmapto('<Plug>PdbStep', 'n')
	nmap <unique> <Leader>3 <Plug>PdbStep
endif

if !hasmapto('<Plug>PdbNext', 'n')
	nmap <unique> <Leader>4 <Plug>PdbNext
endif

if !hasmapto('<Plug>PdbStartup', 'n')
	nmap <unique> <Leader>7 <Plug>PdbStartup
endif

if !hasmapto('<Plug>PdbQuit', 'n')
	nmap <unique> <Leader>8 <Plug>PdbQuit
endif

if !hasmapto('<Plug>PdbBP', 'n')
	nmap <unique> <Leader>9 <Plug>PdbBP
endif

