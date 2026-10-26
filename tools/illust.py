"""팝 스타일 벡터 일러스트 라이브러리 (viewBox 400x400, 굵은 잉크 외곽선)
카테고리 키로 불러 쓰며, 자동 발행 회차에서도 재사용한다."""
K = "#16131A"
S = f'stroke="{K}" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"'

def _wrap(body, bg=None):
    bgr = f'<rect width="400" height="400" fill="{bg}"/>' if bg else ""
    return f'<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">{bgr}{body}</svg>'

def sparkles(col="#fff"):
    return (f'<path d="M58 70 l8 20 l20 8 l-20 8 l-8 20 l-8 -20 l-20 -8 l20 -8z" fill="{col}" {S}/>'
            f'<path d="M335 300 l6 14 l14 6 l-14 6 l-6 14 l-6 -14 l-14 -6 l14 -6z" fill="{col}" {S}/>'
            f'<circle cx="340" cy="80" r="10" fill="{col}" {S}/>')

def burger(bg="#FF6B3D"):
    b = f'''
<ellipse cx="200" cy="330" rx="150" ry="22" fill="{K}" opacity=".18"/>
<path d="M70 250 h260 a20 20 0 0 1 0 40 h-260 a20 20 0 0 1 0 -40z" fill="#F2A541" {S}/>
<path d="M78 222 q122 34 244 0 l6 32 h-256z" fill="#7A3B1E" {S}/>
<path d="M66 214 h268 l-30 34 l-28 -18 l-30 26 l-30 -24 l-30 28 l-30 -26 l-30 22 l-30 -20z" fill="#FFC93C" {S}/>
<path d="M80 196 q30 22 60 4 q30 22 60 2 q30 22 60 2 q30 20 60 -2" fill="none" stroke="#E8401C" stroke-width="14" stroke-linecap="round"/>
<path d="M150 210 q4 26 -6 40" fill="none" stroke="#E8401C" stroke-width="12" stroke-linecap="round"/>
<path d="M260 208 q6 18 0 30" fill="none" stroke="#E8401C" stroke-width="10" stroke-linecap="round"/>
<path d="M66 196 q0 -120 134 -120 q134 0 134 120 z" fill="#E59A3A" {S}/>
<path d="M110 120 q30 -26 80 -28" fill="none" stroke="#FFD27A" stroke-width="12" stroke-linecap="round"/>
<g fill="#FFF3D6" stroke="{K}" stroke-width="4"><ellipse cx="150" cy="140" rx="8" ry="5"/><ellipse cx="200" cy="118" rx="8" ry="5"/><ellipse cx="250" cy="140" rx="8" ry="5"/><ellipse cx="225" cy="165" rx="8" ry="5"/><ellipse cx="170" cy="168" rx="8" ry="5"/></g>'''
    return _wrap(b + sparkles("#FFD43B"), bg)

def icecream_cup(bg="#5CD6A9"):
    b = f'''
<ellipse cx="200" cy="345" rx="120" ry="18" fill="{K}" opacity=".18"/>
<path d="M95 190 h210 l-26 150 h-158z" fill="#fff" {S}/>
<path d="M104 238 h192" stroke="#FF8FB1" stroke-width="18"/><path d="M110 276 h180" stroke="#FFD43B" stroke-width="18"/>
<path d="M95 190 h210 l-26 150 h-158z" fill="none" {S}/>
<path d="M88 192 q-6 -70 70 -80 q30 -50 84 -20 q66 2 70 100 z" fill="#FFF7E4" {S}/>
<path d="M120 150 q40 -40 90 -30 q50 10 70 50 q-60 -20 -160 -20z" fill="#FFEFC2" stroke="{K}" stroke-width="5"/>
<path d="M140 120 q30 30 20 70 M200 108 q10 40 -10 76 M250 120 q-10 40 10 66" fill="none" stroke="#F4B400" stroke-width="10" stroke-linecap="round"/>
<g {S}><rect x="132" y="140" width="40" height="34" rx="12" fill="#fff"/><rect x="214" y="132" width="40" height="34" rx="12" fill="#fff"/><rect x="176" y="160" width="36" height="30" rx="11" fill="#fff"/></g>
<path d="M270 70 l40 -40" stroke="#C98A4B" stroke-width="16" stroke-linecap="round"/><path d="M256 92 q-10 -26 16 -30 q26 0 14 30z" fill="#C98A4B" {S}/>
<circle cx="300" cy="150" r="6" fill="#F4B400"/>'''
    return _wrap(b + sparkles("#fff"), bg)

def cheese_dip(bg="#FFC93C"):
    b = f'''
<ellipse cx="200" cy="345" rx="140" ry="18" fill="{K}" opacity=".18"/>
<path d="M70 220 h260 q-10 120 -130 120 q-120 0 -130 -120z" fill="#4DA8FF" {S}/>
<ellipse cx="200" cy="220" rx="130" ry="34" fill="#FFB000" {S}/>
<path d="M110 222 q20 -14 40 0 q20 14 40 0 q20 -14 40 0 q20 14 40 0" fill="none" stroke="#FFE08A" stroke-width="10" stroke-linecap="round"/>
<path d="M250 210 l70 -150 l40 100 z" fill="#F6C453" {S}/>
<circle cx="300" cy="120" r="6" fill="#E8401C"/><circle cx="320" cy="150" r="5" fill="#E8401C"/>
<path d="M262 200 q4 30 -4 50" fill="none" stroke="#FFB000" stroke-width="16" stroke-linecap="round"/>
<path d="M120 196 q-40 -80 -10 -140 q40 -10 60 30 q20 50 -14 112z" fill="#C8642B" {S}/>
<path d="M118 110 q14 -6 24 6 M112 140 q16 -4 26 8" fill="none" stroke="#E89552" stroke-width="7" stroke-linecap="round"/>
<path d="M150 206 q4 -40 -2 -60" fill="none" stroke="#FFB000" stroke-width="16" stroke-linecap="round"/>'''
    return _wrap(b + sparkles("#fff"), bg)

def yogurt_bottles(bg="#B69CFF"):
    def bottle(x, body, cap):
        return (f'<path d="M{x-34} 150 q0 -30 22 -42 v-28 h24 v28 q22 12 22 42 v170 q0 18 -18 18 h-32 q-18 0 -18 -18z" fill="{body}" {S}/>'
                f'<rect x="{x-16}" y="56" width="32" height="30" rx="8" fill="{cap}" {S}/>'
                f'<rect x="{x-34}" y="200" width="68" height="60" fill="#fff" {S}/>'
                f'<path d="M{x-20} 230 h40" stroke="{body}" stroke-width="10" stroke-linecap="round"/>')
    b = (f'<ellipse cx="200" cy="350" rx="150" ry="18" fill="{K}" opacity=".18"/>'
         + bottle(110, "#6C63FF", "#FFD43B") + bottle(200, "#FF7FA8", "#5CD6A9") + bottle(290, "#FFA25C", "#4DA8FF")
         + f'<circle cx="60" cy="330" r="16" fill="#3A3FB8" {S}/><circle cx="84" cy="342" r="12" fill="#3A3FB8" {S}/>'
         + f'<path d="M330 320 q20 -30 40 0 q-20 34 -40 0z" fill="#E8401C" {S}/>')
    return _wrap(b + sparkles("#FFD43B"), bg)

def nuts_pouch(bg="#4DA8FF"):
    b = f'''
<ellipse cx="200" cy="350" rx="150" ry="18" fill="{K}" opacity=".18"/>
<path d="M90 120 h150 l16 210 h-182z" fill="#D9A866" {S}/>
<path d="M86 120 h158 v-30 h-158z" fill="#C08B4A" {S}/>
<path d="M100 104 h130" stroke="{K}" stroke-width="5" stroke-dasharray="10 8"/>
<rect x="112" y="190" width="104" height="70" rx="12" fill="#fff" {S}/>
<path d="M130 225 h70" stroke="#FF4D2E" stroke-width="12" stroke-linecap="round"/>
<g {S}>
<ellipse cx="275" cy="300" rx="30" ry="18" fill="#C8783A" transform="rotate(-20 275 300)"/>
<ellipse cx="320" cy="330" rx="28" ry="16" fill="#E9B872" transform="rotate(30 320 330)"/>
<path d="M240 330 q-10 -30 20 -36 q30 6 20 36 q-20 14 -40 0z" fill="#8B5A2B"/>
<ellipse cx="340" cy="285" rx="24" ry="14" fill="#C8783A" transform="rotate(10 340 285)"/>
</g>
<circle cx="310" cy="170" r="46" fill="#FFD43B" {S}/><circle cx="310" cy="170" r="30" fill="none" stroke="{K}" stroke-width="5"/>
<path d="M298 160 q12 -10 24 0 q-24 10 0 20 q-12 10 -24 0" fill="none" stroke="{K}" stroke-width="5" stroke-linecap="round"/>
<path d="M360 120 l20 -10 M362 140 l24 0" stroke="{K}" stroke-width="6" stroke-linecap="round"/>'''
    return _wrap(b + sparkles("#fff"), bg)

def basket(bg="#FFD43B"):
    b = f'''
<ellipse cx="200" cy="355" rx="160" ry="18" fill="{K}" opacity=".18"/>
<path d="M100 120 q100 -110 200 0" fill="none" stroke="{K}" stroke-width="16" stroke-linecap="round"/>
<path d="M100 120 q100 -110 200 0" fill="none" stroke="#FF4D2E" stroke-width="8" stroke-linecap="round"/>
<circle cx="150" cy="150" r="46" fill="#E59A3A" {S}/><path d="M104 150 h92" stroke="#FFC93C" stroke-width="12"/>
<path d="M220 100 l36 70 h-72z" fill="#fff" {S}/><circle cx="238" cy="96" r="26" fill="#FF8FB1" {S}/>
<path d="M270 120 v-30 h20 v30 q14 8 14 26 v40 h-48 v-40 q0 -18 14 -26z" fill="#B69CFF" {S}/>
<path d="M60 170 h280 l-30 160 h-220z" fill="#FF4D2E" {S}/>
<path d="M60 170 h280" stroke="{K}" stroke-width="8"/>
<g stroke="#fff" stroke-width="10" stroke-linecap="round" opacity=".9">
<path d="M110 200 l12 100"/><path d="M160 200 l4 100"/><path d="M210 200 v100"/><path d="M260 200 l-4 100"/><path d="M300 200 l-12 100"/></g>
<path d="M60 170 h280 l-30 160 h-220z" fill="none" {S}/>
<circle cx="345" cy="110" r="26" fill="#FFF3B0" {S}/><circle cx="345" cy="110" r="14" fill="none" stroke="{K}" stroke-width="5"/>
<circle cx="50" cy="120" r="20" fill="#FFF3B0" {S}/>'''
    return _wrap(b + sparkles("#fff"), bg)

LIB = {"burger": burger, "icecream": icecream_cup, "cheese": cheese_dip,
       "yogurt": yogurt_bottles, "nuts": nuts_pouch, "basket": basket}

def get(name, bg=None):
    f = LIB[name]
    return f(bg) if bg else f()
