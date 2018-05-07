nnoremap <silent> <Plug>PdbToggle :call pdb#toggle()<CR>
nnoremap <silent> <Plug>PdbBP :call pdb#breakpoint()<CR>
nnoremap <silent> <Plug>PdbNext :call pdb#run(1)<CR>
nnoremap <silent> <Plug>PdbStep :call pdb#run(2)<CR>
nnoremap <silent> <Plug>PdbRun :call pdb#run(0)<CR>
nnoremap <silent> <Plug>PdbPrintCword :call pdb#print(expand('<cword>'))<CR>

if !hasmapto('<Plug>PdbToggle', 'n')
	nmap <unique> <F8> <Plug>PdbToggle
endif

if !hasmapto('<Plug>PdbBP', 'n')
	nmap <unique> <F9> <Plug>PdbBP
endif

if !hasmapto('<Plug>PdbStep', 'n')
	nmap <unique> <Leader>3 <Plug>PdbStep
endif

if !hasmapto('<Plug>PdbNext', 'n')
	nmap <unique> <Leader>4 <Plug>PdbNext
endif

if !hasmapto('<Plug>PdbRun', 'n')
	nmap <unique> <Leader>5 <Plug>PdbRun
endif

if !hasmapto('<Plug>PdbPrintCword', 'n')
	nmap <unique> <Leader>p <Plug>PdbPrintCword
endif

command -nargs=1 PdbPrint call pdb#print('<args>')