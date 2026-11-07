export default function Logo({compact=false}:{compact?:boolean}) {
 return <div className="logo-lockup"><span className="logo-mark"><svg viewBox="0 0 32 32" aria-hidden="true"><path d="M5 7.5h22L10 24.5h17" fill="none" stroke="currentColor" strokeWidth="2.3" strokeLinecap="round" strokeLinejoin="round"/><path d="M5 16h11" fill="none" stroke="currentColor" strokeWidth="2.3" strokeLinecap="round"/></svg></span>{!compact&&<span className="logo-word">PARALLAX<span className="logo-period">.</span></span>}</div>
}
