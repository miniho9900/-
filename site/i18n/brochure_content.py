# 회사소개서(2026) 내용 — AX 관련 내용 제외. 새 문서(NEW)와 기존 문서 변경(UPD)
T = "2026-11-13"
A = {  # asset ids on the claude.ai site
 "msoc":"5acf621b8f0cf23204da1a6702d72af3",
 "iso9001":"7ddbfe1b59e1137a1abc8817cbd7eaf9","iso45001":"52be41d5d7dfc5eed872c7e21122da42","iso14001":"441a11c865e8f3d883c37bfeb0318a90",
 "swbiz":"58ce69fa17dbbf6bee1c4229d03204db","ictcon":"3fe88dc958c48340518163d1bfe15a2a","mainbiz":"a8ac1a6009e027563897cd068e1fb380","innobiz":"6a16baed0a195a81aaa2ef6c261bd46c",
 "lab":"2ac744382aa729b59ccb01c065f40bc0","venture":"5c7f2920280c6905373b770ff5c41851","patent":"564c9b03bbd465bcd7004ce38e924945","gs":"93822599bc16cba38f54b4ded8d15842",
 "security":"d06113b2f770fa3a9bcc318cba7d9a99","techcomp":"c28d00507b7b5c389e64a618e711356e","assembly":"a587d6df2b7b63b2e1b02f8c523d1928","goodict":"2ea47567f55b2808f8b812daab45801c","powerbrand":"453cd42cb554a47f7dbcea958de11dd4",
}
NEW = {}
def doc(path, **kw): NEW[path] = {**kw, "visible": True, "updatedAt": T}

# 연혁 (최신순)
H = [
 ("2026","국회 교육위원장 표창 4년 연속 수상 (지능형 네트워크 솔루션 부문)\n차세대 SDN 컨트롤러 내 ‘양자내성암호(PQC)’ 상용화 적용",
         "National Assembly Education Committee Chair's Commendation — 4th consecutive year (intelligent network solutions)\nPost-quantum cryptography (PQC) applied commercially in the next-generation SDN controller"),
 ("2025","기술역량 우수기업 인증 (한국평가데이터)\n지능형 네트워크 서비스 플랫폼 부문 ‘굿-ICT 대상’ 수상 (대한민국 굿컴퍼니대상)",
         "Certified as a technology-competence excellent company (Korea Enterprise Data)\nGood-ICT Grand Prize for intelligent network service platforms (Korea Good Company Awards)"),
 ("2024","사명 변경 ㈜트리즈엔 (엔에스지 + 트리즈네트웍스 합병)\n국내 학내망 시장 SDN 컨트롤러 점유율 1위\n학내 네트워크 시스템 특허 출원",
         "Renamed TrizN Inc. (merger of NSG and Triz Networks)\nNo. 1 SDN controller share in Korea's school network market\nPatent application for a school network system"),
 ("2023","국내 최초 AE 및 PON 통합 SDN 컨트롤러 개발\nMAIN-Biz, Inno-Biz 중소기업 확인서 인증",
         "Developed Korea's first integrated AE & PON SDN controller\nCertified as a MAIN-Biz and Inno-Biz SME"),
 ("2020","국내 최초 유·무선 통합 SDN 컨트롤러 개발\n기업부설연구소 설립\n광다중화, 통합배선반 직접생산증명 취득",
         "Developed Korea's first wired/wireless integrated SDN controller\nEstablished a corporate R&D center\nDirect production certification for optical multiplexers and integrated patch panels"),
 ("2016","연구개발전담부서 인증 (한국산업기술진흥협회)\n스쿨넷 서비스 구축 감사패 수상",
         "Dedicated R&D department certified (KOITA)\nAppreciation plaque for SchoolNet service deployment"),
 ("2013","엔에스지 설립 (2013.12.31)\n교육정보화(스마트 스쿨, 스쿨넷) 사업",
         "NSG founded (December 31, 2013)\nEducation informatization business (Smart School, SchoolNet)"),
]
for i,(y,t,te) in enumerate(H): doc(f"history/h{y}", year=y, text=t, text_en=te, order=i*10)

# 인증 및 수상
C = [
 ("iso9001","품질경영시스템 (ISO 9001)","Quality Management System (ISO 9001)","인증","Certification",""),
 ("iso45001","안전보건경영시스템 (ISO 45001)","Occupational Health & Safety (ISO 45001)","인증","Certification",""),
 ("iso14001","환경경영시스템 (ISO 14001)","Environmental Management System (ISO 14001)","인증","Certification",""),
 ("gs","GS인증 (1등급)","GS Certification (Grade 1)","인증","Certification",""),
 ("security","보안기능확인서","Security Function Certificate","인증","Certification",""),
 ("patent","특허 등 지식재산권 등록 18건","18 registered patents and other IP","지식재산권","Intellectual property",""),
 ("venture","벤처기업확인서","Venture Business Certificate","기업인증","Company certification",""),
 ("lab","기업부설연구소 인정서","Corporate R&D Center Recognition","기업인증","Company certification",""),
 ("mainbiz","경영혁신형 중소기업 (MAIN-Biz)","Management Innovation SME (MAIN-Biz)","기업인증","Company certification",""),
 ("innobiz","기술혁신형 중소기업 (Inno-Biz)","Technology Innovation SME (Inno-Biz)","기업인증","Company certification",""),
 ("techcomp","기술역량 우수기업 인증","Technology Competence Excellence Certification","기업인증","Company certification","2026"),
 ("swbiz","소프트웨어사업자 관리확인서","Software Business Registration","등록","Registration",""),
 ("ictcon","정보통신공사업 등록증","ICT Construction Business Registration","등록","Registration",""),
 ("assembly","국회 교육위원장 표창 (4년 연속)","National Assembly Education Committee Chair's Commendation (4 years in a row)","수상","Award","2026"),
 ("goodict","Good-ICT Award 대상","Good-ICT Award Grand Prize","수상","Award","2025"),
 ("powerbrand","대한민국 글로벌파워브랜드 대상 (4년 연속)","Korea Global Power Brand Award (4 years in a row)","수상","Award","2026"),
]
for i,(k,t,te,c,ce,y) in enumerate(C): doc(f"works/c_{k}", title=t, title_en=te, category=c, category_en=ce, client="", year=y, imageId=A[k], order=i*10)

# 기술협력 파트너 (회사소개서 기재 순서)
P = [("ARISTA","스위치","arista","8109ea024f48b25743882d22d1d28f28"),("Alcatel-Lucent Enterprise","스위치","alcatel","e0947be5ab16195f14d6b2774ca2d4ac"),("CORE EDGE NETWORKS","스위치","coreedge","6df7fc9d07910d6cc0fc6e5ee8b69fb7"),
 ("HDN (Handreamnet)","스위치","hdn","743d6cc8ba6d412ce17ac75ad77b954d"),("PIOLINK","스위치","piolink","c38e78a8c97ccb3aee2f05d262373eac"),("DASAN","스위치 / OLT / AP","dasan","90908e3ff440ab5c08b62d4b4e7a188d"),
 ("HFR","스위치 / OLT","hfr","7641063a700e3626fc0ecc8d97d795a2"),("TP-Link","스위치 / AP","tplink","a0c515f7fdda50e0f02846a2f57dc9a6"),("NOKIA","OLT","nokia","e0832b0492df8714f12295726250ca02"),
 ("ubiQuoss","스위치 / OLT","ubiquoss","838b885c35ac4e686377fb5aa61d224c"),("AhnLab","UTM","ahnlab","e69855b48745ac49f30c452f7d5978e3"),("AXGATE","UTM / AP","axgate","85633e8ac205d6d1fa9e289bf4314e88"),
 ("FORTINET","UTM / 스위치","fortinet","6572f2523108d68762749bc20d59680a"),("SECUI","UTM","secui","2032efd5f83320c5a2f000ae72baab12"),("DAVOLINK","AP","davolink","b00e126240ca21fe9be389077382e21c"),
 ("에이치원레디오","AP","h1radio","7af721570056d3e060a714a59c318e07"),("KAON BROADBAND","AP","kaon","f063c2df305f0dc2103b66e7cde12b36")]
for i,(n,r,k,aid) in enumerate(P): doc(f"partners/tp_{k}", name=n, role=r, url="", imageId=aid, order=i*10)

# 구축 고객
CL = [("서울특별시교육청","seoul","3b9f94791999571bd49be82b6c27045e"),("대전광역시교육청","daejeon","cf8b89f597d73e81af02be5771cdbf8d"),("인천광역시교육청","incheon","8bbb8cf111abdf03c5e0d764491851eb"),("전남광주통합특별시","jeonnam","2208be5259b9bf594d27eca44cf09944"),
 ("경기도교육청","gyeonggi","a06e8e4a4eb67c73c9f0132d1d781ff9"),("제주특별자치도교육청","jeju","0177eeca9e56c56f20fdcc25259acda5"),("경상남도교육청","gyeongnam","391d2d299bfdf1c52d6706c22cacc3f9"),("강원특별자치도교육청","gangwon","a37835ee0b23c877e74566b30c95686c")]
for i,(n,k,aid) in enumerate(CL): doc(f"clients/edu_{k}", name=n, group="교육청", group_en="Offices of Education", imageId=aid, order=i*10)
CL2 = [("경주시","gyeongju","913306f5ba00500129f68d006ebef76f"),("한국남부발전","kospo","8353e5e47b0c5aa163bf0910993e0ef5"),("한화오션에코텍","hanwha","ca627d4eb2324aea6afd0e13f9e1aa53"),("장안대학교","jangan","f892806e85ad723823c9720bea559a98"),
 ("수원과학대학교","ssc","c2835712974a0473d26bb184381ae011"),("수원중앙병원","suwonhosp","fc03623e578998be3dcd46be92446168"),("sisun","sisun","f4fe0a6db71c91782f31d7db12671a47"),("CHAI","chai","c3e98d55cffa97e0ad0f5e98505e8b0e"),
 ("ANCORS","ancors","2a2a13f6b219c3b9fb2257488ca909cf"),("tdf (The Design Frontier)","tdf","e1d8a4e1dc9236657d6d6f269cab4b36")]
for i,(n,k,aid) in enumerate(CL2): doc(f"clients/cl_{k}", name=n, group="공공·기업·기관", group_en="Public sector, enterprises & institutions", imageId=aid, order=100+i*10)

# 보도자료 (주요 성과)
PR = [
 ("pr20260203","2026-02-03","트리즈엔, 차세대 SDN 컨트롤러에 양자내성암호(PQC) 통합 성공","TrizN integrates post-quantum cryptography (PQC) into its next-generation SDN controller",
  "국민대학교 교수 연구팀이 양자내성암호 알고리즘 ML-KEM을 TLS 1.3 핸드셰이크에 적용한 PQC-TLS 라이브러리를 자체 구현하고, 트리즈엔 상용 제품 적용에 성공했다.",
  "A Kookmin University research team implemented a PQC-TLS library applying the ML-KEM post-quantum algorithm to the TLS 1.3 handshake, and successfully applied it to TrizN's commercial products."),
 ("pr20251127","2025-11-27","트리즈엔-노키아, 차세대 유선 액세스망 고도화 전략적 협력","TrizN and Nokia partner to advance next-generation wired access networks",
  "트리즈엔이 노키아솔루션앤네트웍스코리아(노키아)와 차세대 유선 액세스망 관련 기술 협력 및 제품 개발을 위한 전략적 업무협약(MOU)을 체결했다.",
  "TrizN signed a strategic MOU with Nokia Solutions and Networks Korea for technology cooperation and product development in next-generation wired access networks."),
 ("pr20250822","2025-08-22","트리즈엔, 지능형 네트워크 플랫폼 부문 ‘굿-ICT 대상’ 수상","TrizN wins the Good-ICT Grand Prize for its intelligent network platform",
  "2025 제11회 대한민국 굿컴퍼니 대상에서 ‘지능형 네트워크 서비스 플랫폼’ 부문 ‘굿-ICT 대상(Good-ICT Award)’을 수상했다.",
  "At the 11th Korea Good Company Awards 2025, TrizN received the Good-ICT Award in the intelligent network service platform category."),
 ("pr20250116","2025-01-16","트리즈엔, 대한민국 글로벌 파워브랜드 지능형 네트워크 솔루션 부문 대상","TrizN wins the Korea Global Power Brand Award for intelligent network solutions",
  "제12회 2024 대한민국 글로벌 파워브랜드 대상 시상식에서 지능형 네트워크 솔루션 부문 대상과 국회 교육위원장 표창을 수상했다. 4년 연속 수상이다.",
  "At the 12th Korea Global Power Brand Awards 2024, TrizN received the grand prize in intelligent network solutions and the National Assembly Education Committee Chair's Commendation — its fourth consecutive year."),
]
for i,(k,d,t,te,b,be) in enumerate(PR):
  doc(f"posts/{k}", board="press", date=d, pinned=False, title=t, title_en=te, body=b, body_en=be, bodyHtml=f"<p>{b}</p>", bodyHtml_en=f"<p>{be}</p>", imageId=None, order=-100+i*10)

doc("products/p10", name="SDN 컨트롤러", name_en="SDN Controller", category="SDN 플랫폼", category_en="SDN Platform", featured=True, imageId=None, order=5,
    summary="국내 최초 유·무선 통합 SDN 컨트롤러. 유·무선 네트워크 인프라 전체를 하나의 정책으로 중앙에서 통합 제어합니다.",
    summary_en="Korea's first wired/wireless integrated SDN controller — central, policy-based control of the entire network infrastructure.")

doc("facts/f13", label="기업인증", label_en="Certifications", value="벤처기업, 기업부설연구소,\n경영혁신형(MAIN-Biz), 기술혁신형(Inno-Biz)", value_en="Venture business, corporate R&D center,\nMAIN-Biz, Inno-Biz", icon="award", order=105)
doc("facts/f14", label="ISO 인증", label_en="ISO", value="ISO 9001 · ISO 45001 · ISO 14001", value_en="ISO 9001 · ISO 45001 · ISO 14001", icon="document", order=106)

# 기존 문서 변경 (필드만 덧붙이거나 바꿈)
UPD = {
 "facts/f07": {"value":"9.8억원","value_en":"KRW 980 million"},
 "facts/f09": {"value":"소프트웨어 개발 및 공급, 정보통신공사업,\n네트워크 장비 개발 및 공급, 기간통신사업","value_en":"Software development and supply, ICT construction,\nnetwork equipment development and supply,\nfacilities-based telecommunications"},
 "facts/f11": {"value":"[본사] 경기도 수원시 영통구 대학3로4번길 15\n[지사] 서울시 종로구 인사동5길 29, 태화빌딩 10층 1004호\n[공장] 경기도 수원시 영통구 대학3로 4번길 36","value_en":"[HQ] 15 Daehak 3-ro 4beon-gil, Yeongtong-gu, Suwon-si, Gyeonggi-do\n[Branch] Rm 1004, 10F Taehwa Bldg, 29 Insadong 5-gil, Jongno-gu, Seoul\n[Factory] 36 Daehak 3-ro 4beon-gil, Yeongtong-gu, Suwon-si"},
 "products/p1": {"category":"SDN 플랫폼","category_en":"SDN Platform"},
 "products/p2": {"category":"네트워크 인프라","category_en":"Network Infrastructure"},
 "products/p3": {"category":"네트워크 인프라","category_en":"Network Infrastructure"},
 "products/p4": {"category":"네트워크 인프라","category_en":"Network Infrastructure"},
 "products/p8": {"category":"네트워크 인프라","category_en":"Network Infrastructure"},
 "products/p9": {"category":"네트워크 인프라","category_en":"Network Infrastructure"},
 "posts/n2": {"visible": False},
 "site/config": {
  "aboutTitle":"AI 네트워크 대표기업,\n트리즈엔","aboutTitle_en":"TrizN,\na leader in AI networks",
  "ceoMessage":"국내 지능형 네트워크 시장을 선도해 온 트리즈엔은, 독자적인 SDN 기술과 지속적인 연구개발을 바탕으로 유·무선 네트워크를 통합 관리하고, 보다 지능적인 네트워크 운영을 위한 기술과 솔루션을 발전시켜 왔습니다.\n\n이제 축적된 네트워크 기술에 AI를 더해, 연결을 넘어 지능으로, 네트워크의 새로운 기준을 만들어갑니다.\n\n트리즈엔은 네트워크 구축부터 AI 기반 운영·관리까지, 지능형 네트워크 운영 환경을 구현하는 전문기업입니다.",
  "ceoMessage_en":"TrizN has led Korea's intelligent network market. Built on proprietary SDN technology and continuous R&D, we manage wired and wireless networks as one and keep advancing the technology and solutions for smarter network operations.\n\nNow we are adding AI to our accumulated network technology — moving beyond connection to intelligence, and setting a new standard for networks.\n\nFrom network deployment to AI-based operation and management, TrizN builds intelligent network operating environments.",
  "visionLead":"고객 환경에 최적화된 토탈 네트워크 서비스로 세계 최대 네트워크 서비스 플랫폼을 지향합니다.","visionLead_en":"Total network services optimized for each customer, on the way to becoming the world's largest network service platform.",
  "vision":"Mission · 고객 환경에 최적화된 토탈 네트워크 서비스 제공 | 고객의 복잡하고 다양한 환경에 맞춰 유·무선 네트워크 설치부터 운영, 관리 및 맞춤형 컨설팅과 자동화까지 책임지는 솔루션 개발과 서비스를 제공하겠습니다.\nVision · 세계 최대 네트워크 서비스 플랫폼으로 도약 | 네트워크망의 보유가 아닌 기술과 서비스 경쟁력을 기반으로 글로벌 네트워크 서비스 플랫폼을 지향합니다.\nValue · 전문성 · 고객 중심 · 책임 | 맞춤형 컨설팅부터 운영·관리, 자동화까지 고객의 네트워크 전 과정을 함께합니다.",
  "vision_en":"Mission · Total network services optimized for every customer environment | Tailored to complex and diverse environments, we develop solutions and deliver services covering everything from installing wired and wireless networks to operation, management, consulting and automation.\nVision · Becoming the world's largest network service platform | Not by owning network lines, but through technology and service competitiveness, we aim to be a global network service platform.\nValue · Expertise · Customer focus · Responsibility | From tailored consulting to operation, management and automation, we stay with our customers through every stage of their network.",
  "bizStatusLead":"지능형 네트워크 솔루션 개발부터 장비 제조·구축·통합·운영까지 — 네트워크 전 주기를 자체 역량으로 완결합니다.","bizStatusLead_en":"From intelligent network solution development to equipment manufacturing, deployment, integration and operation — we cover the entire network lifecycle in-house.",
  "bizStatus":"지능형 네트워크 플랫폼 개발 | SDN 기반 통합관리와 AI 기술로 더 스마트한 네트워크 운영을 실현합니다.\n지능형 네트워크 장비 제조 | 자체 기술로 개발하고 엄격한 품질관리와 안정적인 제품을 공급합니다.\n지능형 네트워크 통합 구축 | 전문 컨설팅과 구축 역량으로 최적의 네트워크 환경을 구현합니다.\n지능형 통합 운용·관제 서비스 | 고객 개입이 필요 없는(Touch-Zero) 지능형 SDN 매니지드 서비스를 제공합니다.",
  "bizStatus_en":"Intelligent network platform development | SDN-based integrated management and AI for smarter network operations.\nIntelligent network equipment manufacturing | Developed in-house and supplied as stable products under strict quality control.\nIntelligent network integration | Expert consulting and deployment capabilities for the best network environment.\nIntelligent integrated operations & monitoring | Touch-Zero intelligent SDN managed services that need no customer intervention.",
  "orgLead":"전문성과 책임감을 바탕으로 유기적인 협업 체계를 구축하여 효율적인 의사결정과 실행력을 높이고 있습니다. 고객 가치 실현을 위해 각 분야의 전문가들이 함께합니다.",
  "orgLead_en":"Built on expertise and responsibility, our collaborative structure enables efficient decisions and strong execution. Specialists in every field work together to deliver value to customers.",
  "orgTop":"대표이사","orgTop_en":"CEO","orgStaff":"기획팀 · 총무팀 · 고문","orgStaff_en":"Planning · General Affairs · Advisors",
  "orgChart":"경영총괄 (CFO) | 경영지원본부, 회계팀, 재무팀, 법무팀, IR공시팀, 인사팀\n사업총괄 (CMO) | BS1 본부, BS2 본부, 마케팅 본부, 신사업 본부, 조달 사업부, 사업지원부\n전략총괄 (CSO) | 전략사업 본부\n기술총괄 (CTO) | R&D 본부, TS 본부, 생산기술본부",
  "orgChart_en":"Management (CFO) | Management Support, Accounting, Finance, Legal, IR & Disclosure, HR\nBusiness (CMO) | BS1 Division, BS2 Division, Marketing, New Business, Procurement, Business Support\nStrategy (CSO) | Strategic Business Division\nTechnology (CTO) | R&D Division, TS Division, Production Engineering",
  "orgStats":[{"num":"4","suffix":"개","suffix_en":"","label":"핵심 총괄 체계","label_en":"Core divisions","desc":"경영·사업·전략·기술 분야별 전문 조직 운영","desc_en":"Management, business, strategy and technology"},
              {"num":"85","suffix":"%","label":"전문 인력 비중","label_en":"Specialist staff","desc":"엔지니어, 컨설팅, PMO 등 기술 중심의 인력 구성","desc_en":"Engineers, consultants, PMO and more"},
              {"num":"43","suffix":"%","label":"고급 기술인력 비중","label_en":"Senior engineers","desc":"고급 이상 인력 — 검증된 기술 전문성 보유","desc_en":"Senior-grade or above — proven expertise"},
              {"num":"18","suffix":"명","suffix_en":"","label":"연구소 소속 인력","label_en":"R&D center staff","desc":"기업부설연구소 소속","desc_en":"Corporate R&D center"}],
  "historyLead":"기술 혁신과 신뢰를 바탕으로 성장의 발자취를 이어갑니다.","historyLead_en":"Building on technical innovation and trust, step by step.",
  "caseTitle":"8개 교육청, 약 3,000개 학교\nSDN 구축·운영","caseTitle_en":"8 offices of education,\nabout 3,000 schools on our SDN",
  "caseText":"전국 교육 현장에서 검증된 SDN 기술과 제품 경쟁력을 바탕으로, 자체 네트워크 제품과 기술로 구축부터 운영·관제까지 지원합니다.",
  "caseText_en":"Proven in schools nationwide, our own SDN technology and products support customers from deployment through operations and monitoring.",
  "caseChips":"교육시장 점유율 1위 · 구축·통합 운용·관제 서비스 · 공공 · 교육 · 국방 · 민간","caseChips_en":"No. 1 in the education market · Deployment & managed operations · Public · Education · Defense · Enterprise",
  "caseImageId": A["msoc"],
  "address3":"서울시 종로구 인사동5길 29, 태화빌딩 10층 1004호","address3_en":"Rm 1004, 10F Taehwa Bldg, 29 Insadong 5-gil, Jongno-gu, Seoul, Korea",
  "stats":[{"num":"3,000","suffix":"+","label":"SDN 구축·운영 학교","label_en":"Schools running our SDN"},
           {"num":"8","suffix":"","label":"교육청 SDN 구축","label_en":"Offices of education"},
           {"num":"18","suffix":"건","suffix_en":"","label":"특허 등 지식재산권","label_en":"Patents & IP"},
           {"num":"4","suffix":"년","suffix_en":" yrs","label":"연속 국회 교육위원장 표창","label_en":"Consecutive years of commendation"}],
 },
}
