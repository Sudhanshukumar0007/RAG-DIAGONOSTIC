# RAG Diagnostic - Manual Spot Check

Please review the following 15 rows. Add `CONFIRM` or `CORRECT-TO-X` next to each row.

## Query ID: bihar_q0_en
**Language**: en

**Query**: What is the capital of Bihar?

### Retrieved Context (Top 3 Chunks)
**Chunk 1 (Topic: bihar, Lang: en):**
Bihar (Hindi: Bihār,pronounced [bɪˈɦaːr] ) is a state in eastern India. It borders Uttar Pradesh to its west, Nepal to the north, the northern part of West Bengal to the east, and Jharkhand to the south. Bihar is split by the river Ganges, which flows from west to east. It is the second largest state by population, the 12th largest by area, and the 14th largest by GDP in 2024. The official language on Bihar is Hindi, which shares official status alongside that of Urdu. The main native languages

**Chunk 2 (Topic: bihar, Lang: hi):**
बिहार (بہار) भारत के उत्तर-पूर्वी भाग के मध्य में स्थित एक प्रसिद्ध ऐतिहासिक राज्य है और इसकी राजधानी पटना है। यह जनसंख्या की दृष्टि से भारत का तीसरा सबसे बड़ा प्रदेश है जबकि क्षेत्रफल की दृष्टि से बारहवां है। २००० ई॰ को बिहार के दक्षिणी हिस्से को अलग कर एक नया राज्य झारखण्ड बनाया गया। बिहार के उत्तर में नेपाल, दक्षिण में झारखण्ड, पूर्व में पश्चिम बंगाल और पश्चिम में उत्तर प्रदेश स्थित है। यह क्षेत्र गंगा नदी तथा उसकी सहायक नदियों के उपजाऊ मैदानों में बसा है। गंगा इसमें पश्चिम से पूर्व की तरफ

**Chunk 3 (Topic: bihar, Lang: en):**
Bihar covers a total area of 94,163 km2 (36,357 sq mi), with an average elevation above sea level of 173 feet (53 m). It is landlocked by Nepal in the north, Jharkhand in the south, West Bengal in the east and Uttar Pradesh in the west. It has three parts on the basis of physical and structural conditions: the Southern Plateau, the Shivalik Region, and Bihar's Gangetic Plain. Furthermore, the vast stretch of the fertile Bihar Plain is divided by the Ganges River into two unequal parts – North

### Generated Answer
> Patna.

### Automated Labels
- **retrieval_correct**: N
- **answer_faithful**: hallucinated
- **response_type**: answered_ungrounded

---

## Query ID: rajasthan_q2_hi
**Language**: hi

**Query**: राजस्थान की आधिकारिक भाषा क्या है?

### Retrieved Context (Top 3 Chunks)
**Chunk 1 (Topic: rajasthan, Lang: hi):**
एवं भौगोलिक विशेषताओं के परिचायक नामों से भी पुकारा जाता रहा है। पर तथ्य यह है कि राजस्थान के अधिकांश तत्कालीन क्षेत्रों के नाम वहां बोली जाने वाली प्रमुखतम बोलियों पर ही रखे गए थे। उदाहरणार्थ ढ़ूंढ़ाडी-बोली के इलाकों को ढ़ूंढ़ाड़ (जयपुर) कहते हैं। 'मेवाती' बोली वाले निकटवर्ती भू-भाग अलवर को 'मेवात', उदयपुर क्षेत्र में बोली जाने वाली बोली 'मेवाड़ी' के कारण उदयपुर को मेवाड़, ब्रजभाषा-बाहुल्य क्षेत्र को 'ब्रज', 'मारवाड़ी' बोली के कारण बीकानेर-जोधपुर इलाके को 'मारवाड़' और 'वागडी' बोली पर ही

**Chunk 2 (Topic: rajasthan, Lang: en):**
The languages of Rajasthan primarily belong to the Rajasthani group of Indo-Aryan languages, which most people regard as their own language. In the north are dialects of Punjabi and Bagri, which is a transition between Rajasthani and Punjabi. In the northeast Shekhawati and Dhundari are spoken which gradually merge with Haryanvi. In the east Mewati is spoken in the Mewat region, while in the far east Braj is spoken. To the southeast Haryanvi is spoken. To the west in the heart of the Thar

**Chunk 3 (Topic: uttar_pradesh, Lang: en):**
Hindi became the language of state administration with the Uttar Pradesh Official Language Act of 1951. A 1989 amendment to the act added Urdu, as an additional language of the state. There are numerous language varieties spoken in the state. The north and northwestern parts of the state speak Khadi Boli, the language variety from which Standard Hindi and Urdu developed. In the southwest is spoken Braj Bhasha, seen as the language of Krishna and an important literary language for Krishna Bhakti

### Generated Answer
> ERROR: LLM call failed after 3 attempts.

### Automated Labels
- **retrieval_correct**: N
- **answer_faithful**: N
- **response_type**: error

---

## Query ID: tamil_nadu_q0_hi
**Language**: hi

**Query**: तमिलनाडु की राजधानी क्या है?

### Retrieved Context (Top 3 Chunks)
**Chunk 1 (Topic: tamil_nadu, Lang: en):**
Tamil Nadu is a major centre for music, art and dance in India. Chennai is called the cultural capital of South India. In the Sangam era, art forms were classified into: iyal (poetry), isai (music) and nadakam (drama). Bharatanatyam is a classical dance form that originated in Tamil Nadu and is one of the oldest dances of India. Other regional folk dances include Karakattam, Kavadi, Koodiyattam, Oyilattam, Paraiattam and Puravaiattam. The dance, clothing, and sculptures of Tamil Nadu exemplify

**Chunk 2 (Topic: tamil_nadu, Lang: en):**
Chennai is the capital of the state and houses the state executive, legislative and head of judiciary. The administration of the state government functions through various secretariat departments. There are 43 departments of the state and the departments have further sub-divisions which may govern various undertakings and boards. The state is divided into 38 districts, each of which is administered by a District Collector, who is an officer of the Indian Administrative Service (IAS) appointed

**Chunk 3 (Topic: tamil_nadu, Lang: en):**
Tamil Nadu covers an area of 130,058 km2 (50,216 sq mi) and is the tenth-largest state in India. Located on the south-eastern coast of the Indian peninsula, Tamil Nadu is straddled by the Western Ghats and Deccan Plateau in the west, the Eastern Ghats in the north, the Eastern Coastal Plains lining the Bay of Bengal in the east, the Gulf of Mannar and the Palk Strait to the south-east, and the Laccadive Sea at the southern cape of the peninsula. Politically, Tamil Nadu is bound by the Indian

### Generated Answer
> चेन्नई

### Automated Labels
- **retrieval_correct**: N
- **answer_faithful**: hallucinated
- **response_type**: answered_ungrounded

---

## Query ID: uttar_pradesh_q1_hi
**Language**: hi

**Query**: अगरा, उत्तर प्रदेश में कौन सा प्रसिद्ध स्मारक स्थित है?

### Retrieved Context (Top 3 Chunks)
**Chunk 1 (Topic: gujarat, Lang: en):**
Museums and memorials

**Chunk 2 (Topic: bihar, Lang: hi):**
राजगीर तथा आसपास
राजगृह मगध साम्राज्य की पहली राजधानी तथा हिंदू, जैन एवं बौध धर्म का एक प्रमुख दार्शनिक स्थल है। भगवान बुद्ध तथा वर्धमान महावीर से जुडा कई स्थान अति पवित्र हैं। वेणुवन, सप्तपर्णी गुफा, गृद्धकूट पर्वत, जरासंध का अखाड़ा, गर्म पानी के कुंड, मख़दूम कुंड आदि राजगीर के महत्वपूर्ण दर्शनीय स्थल हैं।
नालंदा तथा आसपास

**Chunk 3 (Topic: bihar, Lang: hi):**
नालंदा विश्वविद्यालय के भग्नावशेष, पावापुरी में भगवान महावीर का परिनिर्वाण स्थल एवं जलमंदिर, बिहारशरीफ में मध्यकालीन किले का अवशेष एवं १४वीं सदी के सूफी संत की दरगाह (बड़ी दरगाह एवं छोटी दरगाह), नवादा के पास ककोलत जलप्रपात। :प्राचीन काल का सबसे लोकप्रिय महाविहार, अकादमिक उत्कृष्टता का एक महत्वपूर्ण बौद्ध केंद्र और आध्यात्मिकता की भावना से ओत-प्रोत एक मामूली तीर्थस्थल, नालंदा वर्तमान में भी समान रूप से समृद्ध स्थान बना हुआ है. यह आध्यात्मिकता, इतिहास, संस्कृति, वास्तुकला और पर्यटन का जीवंत

### Generated Answer
> The context does not contain enough information to answer this question.

### Automated Labels
- **retrieval_correct**: N
- **answer_faithful**: Y
- **response_type**: refused

---

## Query ID: rajasthan_q0_hi
**Language**: hi

**Query**: राजस्थान की राजधानी क्या है?

### Retrieved Context (Top 3 Chunks)
**Chunk 1 (Topic: uttar_pradesh, Lang: hi):**
उत्तर प्रदेश (अंग्रेज़ी: Uttar Pradesh) भारत का सबसे बड़ा (जनसंख्या के आधार पर) राज्य और क्षेत्रफल की दृष्टि के आधार पर चौथा सबसे बड़ा राज्य है। लखनऊ प्रदेश की प्रशासनिक व विधायिक राजधानी है और प्रयागराज न्यायिक राजधानी है। आगरा, कानपुर, वाराणसी, एवं गोरखपुर प्रदेश के अन्य महत्त्वपूर्ण शहर हैं। राज्य के उत्तर में उत्तराखण्ड तथा हिमाचल प्रदेश, पश्चिम में हरियाणा, दिल्ली तथा राजस्थान, दक्षिण में मध्य प्रदेश तथा छत्तीसगढ़ और पूर्व में बिहार तथा झारखंड राज्य स्थित हैं। इनके अतिरिक्त राज्य की उत्तर

**Chunk 2 (Topic: uttar_pradesh, Lang: hi):**
सीमेण्ट से बने घर, पक्की सड़कें, बिजली, रेडियो, टेलीविजन जैसी उपभोक्ता वस्तुएँ पारम्परिक ग्रामीण जीवन को बदल रही हैं। शहरी जनसंख्या का आधे से अधिक हिस्सा एक लाख से अधिक जनसंख्या वाले शहरों में रहता है। लखनऊ, वाराणसी (बनारस), आगरा, कानपुर, मेरठ, गोरखपुर, और प्रयागराज उत्तर प्रदेश के सात सबसे बड़े नगर हैं। कानपुर उत्तर प्रदेश के मध्य क्षेत्र में स्थित प्रमुख औद्योगिक शहर है। कानपुर के पूर्वोत्तर में 82 किलोमीटर की दूरी पर राज्य की राजधानी लखनऊ स्थित है। हिन्दुओं का सर्वाधिक पवित्र शहर अयोध्या

**Chunk 3 (Topic: rajasthan, Lang: en):**
The State of Rajasthan was formed on 30 March 1949 when the states of the Rajputana Agency of the erstwhile British Empire in India were merged into the new Indian Union. Its capital and largest city is Jaipur. Other important cities are Jodhpur, Kota, Bikaner, Ajmer, Bhilwara, Sawai Madhopur, Bharatpur and Udaipur. The economy of Rajasthan is the seventh-largest state economy in India with ₹10.20 lakh crore (US$110 billion) in gross domestic product and a per capita GDP of ₹118,000 (US$1,200).

### Generated Answer
> राजस्थान की राजधानी जयपुर है।

### Automated Labels
- **retrieval_correct**: N
- **answer_faithful**: hallucinated
- **response_type**: answered_ungrounded

---

## Query ID: rajasthan_q1_hinglish
**Language**: hinglish

**Query**: Rajasthan mein kaun sa desert hai?

### Retrieved Context (Top 3 Chunks)
**Chunk 1 (Topic: rajasthan, Lang: en):**
and rassgullas from Bikaner. Originating from the Marwar region of the state is the concept of Marwari Bhojnalaya or vegetarian restaurants, today found in many parts of India, which offer vegetarian food popular among Marwari people. Ghee is an essential ingredient in most Rajasthani cuisines, and dollops of ghee are poured over food as a welcoming gesture for guests. Dal-baati-churma is very popular in Rajasthan. The traditional way to serve it is to first coarsely mash the baati, and then

**Chunk 2 (Topic: gujarat, Lang: hi):**
कोली : कोली और भील जनजाति इतिहास के कई युद्ध में एक साथ देखी ।
काठी दरबार : काठी दरबार गुजरात की प्रमुख जातियों में से एक है।
राजपूत :राजपूत जाति गुजरात में पाई जाने वाले जातियों में से एक है।
रबारी :रबारी समाज मूल मालधारी है ये भेस,बकरी, भेड़, उट, चराते है। रबारी समाज मूल राजस्थान है ।

इन्हें भी देखें
गुजरात के लोकसभा सदस्य
धोलावीरा
रन ऑफ कच्छ

सन्दर्भ
बाहरी कड़ियाँ

**Chunk 3 (Topic: rajasthan, Lang: hi):**
महर्षि दयानंद सरस्वती विश्वविद्यालय अजमेर
मौलाना अबुल कलाम आजाद विश्वविद्यालय जोधपुर
शेखावाटी विश्वविद्यालय सीकर

### Generated Answer
> The context does not contain enough information to answer this question.

### Automated Labels
- **retrieval_correct**: N
- **answer_faithful**: Y
- **response_type**: refused

---

## Query ID: punjab_q0_hinglish
**Language**: hinglish

**Query**: Punjab ki rajdhani kya hai?

### Retrieved Context (Top 3 Chunks)
**Chunk 1 (Topic: rajasthan, Lang: hi):**
महर्षि दयानंद सरस्वती विश्वविद्यालय अजमेर
मौलाना अबुल कलाम आजाद विश्वविद्यालय जोधपुर
शेखावाटी विश्वविद्यालय सीकर

**Chunk 2 (Topic: rajasthan, Lang: hi):**
(जालोर) सिरोही, कोटा, बूंदी, जयपुर, अलवर,  करौली, झालावाड़ , मेरवाड़ा और टोंक(मुस्लिम पिण्डारी)  राजा महाराणा प्रतापऔर महाराणा सांगा,महाराजा सूरजमल, महाराजा जवाहर सिंह, वीर तेजाजी अपनी असाधारण राज्यभक्ति और शौर्य के लिये जाने जाते है।  पन्ना धाय जैसी बलिदानी माता, मीरां जैसी    जोगिन यहां की एक बड़ी शान है।कर्मा बाई जैसी भक्तणी जिसने भगवान जगन नाथ जी को हाथों से खीचड़ा (खिचड़ी) खिलाया था। इन राज्यों के नामों के साथ-साथ इनके कुछ भू-भागों को स्थानीय एवं भौगोलिक विशेषताओं के परिचायक नामों से भी

**Chunk 3 (Topic: gujarat, Lang: hi):**
कोली : कोली और भील जनजाति इतिहास के कई युद्ध में एक साथ देखी ।
काठी दरबार : काठी दरबार गुजरात की प्रमुख जातियों में से एक है।
राजपूत :राजपूत जाति गुजरात में पाई जाने वाले जातियों में से एक है।
रबारी :रबारी समाज मूल मालधारी है ये भेस,बकरी, भेड़, उट, चराते है। रबारी समाज मूल राजस्थान है ।

इन्हें भी देखें
गुजरात के लोकसभा सदस्य
धोलावीरा
रन ऑफ कच्छ

सन्दर्भ
बाहरी कड़ियाँ

### Generated Answer
> The context does not contain enough information to answer this question.

### Automated Labels
- **retrieval_correct**: N
- **answer_faithful**: Y
- **response_type**: refused

---

## Query ID: punjab_q1_hinglish
**Language**: hinglish

**Query**: Kaun si nadi ne Punjab ka naam diya?

### Retrieved Context (Top 3 Chunks)
**Chunk 1 (Topic: bihar, Lang: hi):**
बिहार सरकार गैनाहा पारसा

**Chunk 2 (Topic: gujarat, Lang: hi):**
कोली : कोली और भील जनजाति इतिहास के कई युद्ध में एक साथ देखी ।
काठी दरबार : काठी दरबार गुजरात की प्रमुख जातियों में से एक है।
राजपूत :राजपूत जाति गुजरात में पाई जाने वाले जातियों में से एक है।
रबारी :रबारी समाज मूल मालधारी है ये भेस,बकरी, भेड़, उट, चराते है। रबारी समाज मूल राजस्थान है ।

इन्हें भी देखें
गुजरात के लोकसभा सदस्य
धोलावीरा
रन ऑफ कच्छ

सन्दर्भ
बाहरी कड़ियाँ

**Chunk 3 (Topic: rajasthan, Lang: hi):**
(जालोर) सिरोही, कोटा, बूंदी, जयपुर, अलवर,  करौली, झालावाड़ , मेरवाड़ा और टोंक(मुस्लिम पिण्डारी)  राजा महाराणा प्रतापऔर महाराणा सांगा,महाराजा सूरजमल, महाराजा जवाहर सिंह, वीर तेजाजी अपनी असाधारण राज्यभक्ति और शौर्य के लिये जाने जाते है।  पन्ना धाय जैसी बलिदानी माता, मीरां जैसी    जोगिन यहां की एक बड़ी शान है।कर्मा बाई जैसी भक्तणी जिसने भगवान जगन नाथ जी को हाथों से खीचड़ा (खिचड़ी) खिलाया था। इन राज्यों के नामों के साथ-साथ इनके कुछ भू-भागों को स्थानीय एवं भौगोलिक विशेषताओं के परिचायक नामों से भी

### Generated Answer
> The context does not contain enough information to answer this question.

### Automated Labels
- **retrieval_correct**: N
- **answer_faithful**: Y
- **response_type**: refused

---

## Query ID: rajasthan_q2_en
**Language**: en

**Query**: What is the official language of Rajasthan?

### Retrieved Context (Top 3 Chunks)
**Chunk 1 (Topic: rajasthan, Lang: en):**
The languages of Rajasthan primarily belong to the Rajasthani group of Indo-Aryan languages, which most people regard as their own language. In the north are dialects of Punjabi and Bagri, which is a transition between Rajasthani and Punjabi. In the northeast Shekhawati and Dhundari are spoken which gradually merge with Haryanvi. In the east Mewati is spoken in the Mewat region, while in the far east Braj is spoken. To the southeast Haryanvi is spoken. To the west in the heart of the Thar

**Chunk 2 (Topic: uttar_pradesh, Lang: en):**
Uttar Pradesh is a linguistically diverse state where several Indo-Aryan languages and dialects are widely spoken. The primary official language is Hindi, used in government, education, and media, and it is also the most widely spoken language across the state. A significant portion of the population speaks various regional languages grouped under the Hindi. These include Awadhi, spoken in Awadh in central Uttar Pradesh; Bhojpuri spoken in Purvanchal in eastern Uttar Pradesh; and Braj Bhasha

**Chunk 3 (Topic: bihar, Lang: hi):**
हिंदी बिहार की राजभाषा और उर्दू द्वितीय राजभाषा है।मैथिली भारतीय संविधान के अष्टम अनुसूची में सम्मिलित एकमात्र बिहारी भाषा है।भोजपुरी, मगही, अंगिका तथा बज्जिका बिहार में बोली जाने वाली अन्य प्रमुख भाषाओं और बोलियों में सम्मिलित हैं।प्रमुख पर्वों में छठ, होली, दीपावली, दशहरा, महाशिवरात्रि, नागपंचमी, श्री पंचमी, मुहर्रम, ईद,तथा क्रिसमस हैं। सिक्खों के दसवें गुरु गोबिन्द सिंह जी का जन्म स्थान होने के कारण पटना सिटी (पटना) में उनकी जयन्ती पर भी भारी श्रद्धार्पण देखने को मिलता है। बिहार ने हिंदी को

### Generated Answer
> ERROR: LLM call failed after 3 attempts.

### Automated Labels
- **retrieval_correct**: N
- **answer_faithful**: N
- **response_type**: error

---

## Query ID: bihar_q1_hinglish
**Language**: hinglish

**Query**: Bihar mein kaun si prachin university thi?

### Retrieved Context (Top 3 Chunks)
**Chunk 1 (Topic: gujarat, Lang: en):**
Universities

**Chunk 2 (Topic: punjab, Lang: en):**
Colleges and universities

**Chunk 3 (Topic: bihar, Lang: hi):**
प्रशासन

### Generated Answer
> The context does not contain enough information to answer this question.

### Automated Labels
- **retrieval_correct**: N
- **answer_faithful**: Y
- **response_type**: refused

---

## Query ID: kerala_q0_hinglish
**Language**: hinglish

**Query**: Kerala ki capital kya hai?

### Retrieved Context (Top 3 Chunks)
**Chunk 1 (Topic: kerala, Lang: en):**
Renaming to Keralam

**Chunk 2 (Topic: kerala, Lang: en):**
References
Notes
Sources
Further reading
Bose, Satheese Chandra and Varughese, Shiju Sam (eds.) 2015. Kerala Modernity: Ideas, Spaces and Practices in Transition. Hyderabad: Orient Blackswan.
Chathukulam, Jos; Tharamangalam, Joseph (2021). "The Kerala model in the time of COVID19: Rethinking state, society and democracy". World Development. 137 105207. doi:10.1016/j.worlddev.2020.105207. PMC 7510531. PMID 32989341.

**Chunk 3 (Topic: kerala, Lang: en):**
Kerala, officially Keralam (Malayalam: [ˈkeːɾɐɭɐm]  Kēraḷam), is a state on the Malabar Coast of southern India. It was formed on 1 November 1956 under the States Reorganisation Act, which unified the country's Malayalam-speaking regions into a single state. Covering 38,863 km2 (15,005 sq mi), Kerala is primarily a strip of coastal plains sandwiched by the Western Ghats and the Laccadive Sea, bound by Karnataka to the northeast, Tamil Nadu to the east, and the Lakshadweep islands in the western

### Generated Answer
> Thiruvananthapuram.

### Automated Labels
- **retrieval_correct**: N
- **answer_faithful**: hallucinated
- **response_type**: answered_ungrounded

---

## Query ID: maharashtra_q1_hi
**Language**: hi

**Query**: महाराष्ट्र में कौन सा नृत्य रूप प्रसिद्ध है?

### Retrieved Context (Top 3 Chunks)
**Chunk 1 (Topic: maharashtra, Lang: en):**
Marathi dance forms draw from folk traditions. Lavani is popular form of dance in the state. The Bhajan, Kirtan and Abhangas of the Warkari sect (Vaishanav Devotees) have a long history and are part of their daily rituals. Koli dance (called 'Koligeete') is among the most popular dances of Maharashtra. As the name suggests, it is related to the fisher folk of Maharashtra, who are called Koli. Popular for their unique identity and liveliness, their dances represent their occupation. This type of

**Chunk 2 (Topic: kerala, Lang: en):**
Kerala is home to a number of performance arts. These include five classical dance forms: Kathakali, Mohiniyattam, Koodiyattom, Thullal and Krishnanattam, which originated and developed in the temple theatres during the classical period under the patronage of royal houses. Kerala natanam, Thirayattam, Kaliyattam, Theyyam, Koothu and Padayani are other dance forms associated with the temple culture of the region. Some traditional dance forms such as Oppana and Duffmuttu were popular among the

**Chunk 3 (Topic: uttar_pradesh, Lang: hi):**
अधिकांश हिस्सा इस काल के दौरान उत्तर प्रदेश में विकसित हुआ। तानसेन व बैजू बावरा जैसे संगीतज्ञ मुग़ल शहंशाह अकबर के दरबार में थे, जो राज्य व समूचे देश में आज भी विख्यात हैं। भारतीय संगीत के दो सर्वाधिक प्रसिद्ध वाद्य सितार (वीणा परिवार का तंतु वाद्य) और तबले का विकास इसी काल के दौरान इस क्षेत्र में हुआ। 18वीं शताब्दी में उत्तर प्रदेश में वृन्दावन व मथुरा के मन्दिरों में भक्तिपूर्ण नृत्य के तौर पर विकसित शास्त्रीय नृत्य शैली कथक उत्तरी भारत की शास्त्रीय नृत्य शैलियों में सर्वाधिक प्रसिद्ध है।

### Generated Answer
> महाराष्ट्र में प्रसिद्ध नृत्य रूप **लावणी** है।

### Automated Labels
- **retrieval_correct**: N
- **answer_faithful**: hallucinated
- **response_type**: answered_ungrounded

---

## Query ID: uttar_pradesh_q0_en
**Language**: en

**Query**: What is the capital of Uttar Pradesh?

### Retrieved Context (Top 3 Chunks)
**Chunk 1 (Topic: uttar_pradesh, Lang: hi):**
उत्तर प्रदेश (अंग्रेज़ी: Uttar Pradesh) भारत का सबसे बड़ा (जनसंख्या के आधार पर) राज्य और क्षेत्रफल की दृष्टि के आधार पर चौथा सबसे बड़ा राज्य है। लखनऊ प्रदेश की प्रशासनिक व विधायिक राजधानी है और प्रयागराज न्यायिक राजधानी है। आगरा, कानपुर, वाराणसी, एवं गोरखपुर प्रदेश के अन्य महत्त्वपूर्ण शहर हैं। राज्य के उत्तर में उत्तराखण्ड तथा हिमाचल प्रदेश, पश्चिम में हरियाणा, दिल्ली तथा राजस्थान, दक्षिण में मध्य प्रदेश तथा छत्तीसगढ़ और पूर्व में बिहार तथा झारखंड राज्य स्थित हैं। इनके अतिरिक्त राज्य की उत्तर

**Chunk 2 (Topic: uttar_pradesh, Lang: en):**
Uttar Pradesh (UTT-ər prə-DESH, abbr. UP; Hindi: Uttar Pradēś, pronounced [ˈʊt̪ːəɾ pɾə.ˈdeːɕ] , lit. 'Northern Province') is a state in northern India. With over 241 million inhabitants, it is India's  most populated state. The state is bordered by Rajasthan to the west, Haryana, Himachal Pradesh and Delhi to the northwest, Uttarakhand and Nepal to the north, Bihar to the east, Madhya Pradesh, Chhattisgarh and Jharkhand to the south. It is the fourth-largest Indian state by area covering 243,286

**Chunk 3 (Topic: uttar_pradesh, Lang: en):**
Uttar Pradesh, with a total area of 240,928 km2 (93,023 sq mi), is India's fourth-largest state in terms of land area and is roughly of same size as United Kingdom. It is situated on the northern spout of India and shares an international boundary with Nepal. The Himalayas border the state on the north, but the plains that cover most of the state are distinctly different from those high mountains. The larger Gangetic Plain region is in the north; it includes the Ganges-Yamuna Doab, the Ghaghra

### Generated Answer
> Lucknow.

### Automated Labels
- **retrieval_correct**: N
- **answer_faithful**: hallucinated
- **response_type**: answered_ungrounded

---

## Query ID: punjab_q0_hi
**Language**: hi

**Query**: पंजाब की राजधानी क्या है?

### Retrieved Context (Top 3 Chunks)
**Chunk 1 (Topic: punjab, Lang: en):**
province of Punjab. Chandigarh serves as a shared capital for Punjab as well as Haryana. The state covers an area of 50,362 square kilometres (19,445 square miles), which is 1.53% of India's total geographical area, making it the 19th-largest Indian state by area out of 28 Indian states (20th largest, if Union Territories are considered). With over 27 million inhabitants, Punjab is the 16th-largest Indian state by population, comprising 23 districts. Punjabi, written in the Gurmukhi script, is

**Chunk 2 (Topic: punjab, Lang: en):**
Punjab is in northwestern India and has a total area of 50,362 square kilometres (19,445 mi2). Punjab is bordered by Pakistan's Punjab province on the west, Jammu and Kashmir on the north, Himachal Pradesh on the northeast and Haryana and Rajasthan on the south. Most of Punjab lies in a fertile, alluvial plain with perennial rivers and an extensive irrigation canal system. A belt of undulating hills extends along the northeastern part of the state at the foot of the Himalayas. Its average

**Chunk 3 (Topic: punjab, Lang: en):**
The capital of Punjab is Chandigarh, which also serves as the capital of Haryana and is thus administered separately as a union territory of India. The judicial branch of the state government is provided by the Punjab and Haryana High Court in Chandigarh.

### Generated Answer
> चंडीगढ़

### Automated Labels
- **retrieval_correct**: N
- **answer_faithful**: hallucinated
- **response_type**: answered_ungrounded

---

## Query ID: kerala_q1_hinglish
**Language**: hinglish

**Query**: Kerala ki sabse lambi nadi kaun si hai?

### Retrieved Context (Top 3 Chunks)
**Chunk 1 (Topic: kerala, Lang: en):**
Kerala's western coastal belt is relatively flat compared to the eastern region, and is criss-crossed by a network of interconnected brackish canals, lakes, estuaries, and rivers known as the Kerala Backwaters. Kuttanad, also known as The Rice Bowl of Kerala, has the lowest altitude in India, and is also one of the few places in world where cultivation takes place below sea level. The country's longest lake Vembanad, dominates the backwaters; it lies between Alappuzha and Kochi and is about 200

**Chunk 2 (Topic: gujarat, Lang: hi):**
कोली : कोली और भील जनजाति इतिहास के कई युद्ध में एक साथ देखी ।
काठी दरबार : काठी दरबार गुजरात की प्रमुख जातियों में से एक है।
राजपूत :राजपूत जाति गुजरात में पाई जाने वाले जातियों में से एक है।
रबारी :रबारी समाज मूल मालधारी है ये भेस,बकरी, भेड़, उट, चराते है। रबारी समाज मूल राजस्थान है ।

इन्हें भी देखें
गुजरात के लोकसभा सदस्य
धोलावीरा
रन ऑफ कच्छ

सन्दर्भ
बाहरी कड़ियाँ

**Chunk 3 (Topic: kerala, Lang: en):**
These southern territories once shared a common language and cultural framework, within a region historically known as Tamilakam. While the Cheras governed most of what is now Kerala, the southern tip of the region fell under the control of the Pandyas, whose trading port is sometimes identified in ancient Western sources as Nelcynda (or Neacyndi). Later, control of the region alternated among the Pandyas, Cheras, and Cholas. The Ays and Mushikas were two other dynasties of ancient Kerala,

### Generated Answer
> The context does not contain enough information to answer this question.

### Automated Labels
- **retrieval_correct**: N
- **answer_faithful**: Y
- **response_type**: refused

---

