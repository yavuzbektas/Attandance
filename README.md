Proje Özeti 

Projemiz Covid-19 pandemisi nedeniyle giriş çıkışın yoğun olduğu okullarda ateş ölçümlerinin
hızlı ve güvenilir bir şekilde yapılmasını sağlamak, HES kodunun sistemde kayıtlı ise yüz tanındığı anda 
sistemden kişinin verisine erişip sağlık bakanlığı sistemine bağlanarak kontrolünün otomatik  yapılması, 
otomatik kaydının tutulması ve risk durumlarında ise  ilgili kişilere bilgi vermek amacıyla yapılmıştır. 
Okula girişlerde sisteme kayıtlı olamayan kişilerin de HES kodunun kamerada QR kod okutularak yaptırılması 
ve ateş ölçümüyle beraber kontrollerin tamamlanması ile güvenli ve hızlı bir şekilde yapıla bilinecektir. 
Böylece giriş çıkışlardaki yoğunluğu azaltmak, termal ölçümü yapan kişilerin yapacağı ölçme ve not etme 
hatalarını kaldırmak, el tipi ateş ölçerlerin sınırlı bir kullanım alanı olması ve çevresel faktörlerden 
çok etkilenmeleri sebebiyle bu proje ortaya çıkarılmıştır. Projemiz aslında sadece okul giriş çıkışlarında 
değil gün içerisinde belli noktalarda koyularak sürekli bir takip sistemi yapıla bilinecektir. Yüzler daha
önce sisteme girilmiş olduğundan hızlı bir şekilde kişi tanımlanacak ve sisteme kaydı tutturulacaktır. 
Yüz tanıma Python dilinde yazılmış olup Derin öğrenme mantığı kullanarak modellenmiş ve ARM işlemcili 
bir kontrol sistemiyle de kamera ve ısı algılayıcısından gelen bilgiler işlenip, ağ üzerinde istenilen 
bir noktaya veri tabanında kayıt tuta bilecektir. İstenildiği anda kayıtlar Excel ortamına aktarıla bilinecektir.  
Anahtar Kelimeler: Covid-19,Ateş Ölçer, Yüz Tanıma, Giriş Çıkış Kontrol, Python

Fonksiyonlar : 
Yüz Tanıma Fonksiyonu : Cihazımız okul girişine koyulması durumunda, okula giren kişilerin cihaza yüzlerini göstermeleri istenecektir. 
Cihaz gördüğü yüzü veri tabanında yer alan diğer yüzler ile karşılaştıracak ve bulması durumunda kişinin ismi ekranda görünmektedir. 
Eğer kişi veri tabanındaki kişiler ile örtüşmüyor ise uyarı vermekte ve güvenlik birimine bildirmektedir.

Isı Ölçme Fonksiyonu : Yüzünü yaklaştıran kişinin ısısını anlık olarak ölçerek ekranda kişinin sıcaklık değerini hemen göstermektedir. 
Risk durumunda güvenlik birimine bildirecektir. 


HES Kodu kontrol Fonksiyonu : Yüzünü tanıdığı kişilerin daha önceden alınmış olan HES kodlarını internet vasıtası ile Sağlık bakanlığı 
sistemine sorgulamakta ve oradan aldığı riskli veya sağlıklı bilgisini anında ekrana yansıtılabilmektedir. 


Otomatik Durum Bildirimi Fonksiyonu : Herhangi bir risk durumunda riskin türüyle beraber güvenlik birimine veya yönetimdeki herhangi 
birine durum anında raporlanabilmektedir. 


Raporlama Fonksiyonu : Belirli periyotlarda veya istenilen bir anda tüm kayıtlar ilgili birim tarafından alınabilmektedir. 




Çift Ekran Desteği : Birincil ekranda Güvenlik birimi tarafından gelen bildiriler takip edilebilmekte ve ikincil ekranda ise yüzü tanınan kişinin bakabileceği ve sıcaklık HES değerlendirme bilgileri ekranda yansıtıla bilmektedir.  

