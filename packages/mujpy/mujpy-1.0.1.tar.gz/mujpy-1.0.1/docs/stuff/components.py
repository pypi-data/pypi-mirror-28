_help_ = {'bl':r'Lorentz decay: $\mbox{asymmetry}\exp(-\mbox{Lor_rate}t)$',
             'bg':r'Gauss decay: $\mbox{asymmetry}\exp(-0.5(\mbox{Gau_rate}t)^2)$',
             'bs':r'Gauss decay: $\mbox{asymmetry}\exp(-0.5(\mbox{rate}t)^\beta)$',
             'da':r'Linearized dalpha correction: $f = \frac{2f_0(1+\alpha/\mbox{dalpha})-1}{1-f_0+2\alpha/dalpha}$',
             'mg':r'Gauss decay: $\mbox{asymmetry}\cos[2\pi(\gamma_\mu \mbox{field} t +\mbox{phase}/360)]\exp(-0.5(\mbox{Gau_rate}t)^2)$',
             'ml':r'Gauss decay: $\mbox{asymmetry}\cos[2\pi(\gamma_\mu \mbox{field} t +\mbox{phase}/360)]\exp(-\mbox{Lor_rate}t)$',
             'ms':r'Gauss decay: $\mbox{asymmetry}\cos[2\pi(\gamma_\mu \mbox{field} t +\mbox{phase}/360)]\exp(-(\mbox{rate}t)^\beta)$',
             'jg':r'Gauss Bessel: $\mbox{asymmetry} j_0[2\pi(\gamma_\mu \mbox{field} t +\mbox{phase}/360)]\exp(-0.5(\mbox{Lor_rate}t)^2)$',
             'jl':r'Lorentz Bessel: $\mbox{asymmetry}j_0[2\pi(\gamma_\mu \mbox{field} t +\mbox{phase}/360)]\exp(-0.5(\mbox{Lor_rate}t)^2)$',
             'fm':r'FMuF: $\mbox{asymmetry}/6[3+\cos 2*\pi\gamma_\mu\mbox{dipfield}\sqrt{3} t + \
       (1-1/\sqrt{3})\cos \pi\gamma_\mu\mbox{dipfield}(3-\sqrt{3})t + \
       (1+1/\sqrt{3})\cos\pi\gamma_\mu\mbox{dipfield}(3+\sqrt{3})t ]\exp(-\mbox{Lor_rate}t)$', 
             'kg':r'Gauss Kubo-Toyabe: static and dynamic, in zero or longitudinal field by G. Allodi [Phys Scr 89, 115201]'}
print(r'{}\n'.format([_help_[k] for k in _help_.keys()]))
