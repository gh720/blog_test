#!perl
($\,$/)=$/;
$_=<>;
if (m{/\*.*?\[debug\]:(\d*)}) {
	if ($1 > 0) {
		s{\}\s*$}{ outline: 1px #dd0000 dashed; \} }gm;
	}
}
print $_;
	