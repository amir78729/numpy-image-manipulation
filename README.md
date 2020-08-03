# numpy image manipulation
### <div dir="rtl">شرح پروژه </div>
<div dir="rtl">
در بسیاری از مسائلی که در حوزه ی پزشکی ، اقتصاد و ... مطرح میشود برای حل مسئله و تصمیم گیری
درمورد موضوع مورد نظر نمونه گیری هایی از جامعه مورد سوال انجام میشود بعنوان مثال در حوزه ی پزشکی
، محیط زیست ، امنیت یا مدیریت شهری ؛ در بسیاری از مواقع نیاز به عکس برداری از نواحی مختلف با
استفاده از دستگاه های مختلف است این عکس ها بصورت ماتریس ذخیره میشوند. یک عکس بطور دارای
۲۰۰۰ در ۲۰۰۰ پیکسل است بنابراین یک عکس بطور معمول دارای ۴ میلیون پیکسل میباشد که بصورت یک
ماتریس با ۳ سطر و ۴ میلیون ستون ذخیره میشود. در هر بررسی این داده ها داده ی خام مسئله هستند که
مورد استفاده مستقیم قرار نمیگیرند بلکه عملیات هایی بر روی اطلاعات اولیه انجام میشود که داده را آماده
ی استفاده برای مراحل حل مسئله میکند. به مجموعه ی این عملیات ها پیش پردازش میگویند.
یکی از راه های پیش پردازش داده ها استفاده از مفاهیم آماری چون میانگین ، واریانس و ... میباشد.
 </div>

### <div dir="rtl"> مراحل پروژه </div> ###
> یک عکس از ناحیه ی مورد نظر خود بگیرید 

در ابتدای برنامه با صفحه ی زیر مواجه خواهیم شد:
```
Hi! How do you want to work with this 
program?
 1 - using ready image
 2 - using another image
-1 - exit the program
please enter your choice:  
```
با انتخاب 1 و 2 نوع ورودی دادن به برنامه مشخص خواهد شد بعد از انجام عملیات روی عکس (در صورت وجود در پوشه موردنظر که خود فایل پروژه هم در آن قرار دارد) تا زمانی که ورودی 1- را به برنامه ندهیم برنامه اجرا خواهد شد و عکس ها را بصورت متوالی از ما دریافت خواهد کرد. عکسی که به صورت پیشفرض برای برنامه در نظر گرفته شده است عکس زیر میباشد:

<img src="https://cdn.discordapp.com/attachments/732234196487241741/734420271972220959/1.jpg">

> آن را بصورت ماتریس ذخیره کنید.

پس از انتخاب عکس آن را به کمک تغییر اندازه به یک عکس 2000×2000 پیکسل تبدیل میکنیم(واضح است که اگر عکسی در ابتدا  بصورت مستطیلی باشد، پس از این عملیات بصورت عمودی یا افقی فشرده خواهد شد تا بصورت مربعی تبدیل شود، مانند شکل زیر که فشرده شده ی عکس بالا میباشد).

<img src="https://cdn.discordapp.com/attachments/732234196487241741/734420298245603338/2.jpg">

سپس آرایه ای دو بعدی از عکس ورودی میسازیم

```python
image_matrix = np.array(image) 
image_matrix.resize((h * w, 3))
```

( h = w = 2000 )

در آرایه‌ی دو بعدی به دست آمده هر یک از ۴۰۰۰۰۰۰ سطر متعلق به یکی از پیکسل های عکس ورودی خواهند بود و هر کدام از این پیکسل ها سه مولفه خواهند داشت که میتوانند رنگ پیکسل را بر اساس سه رنگ قرمز و سبز و آبی بیان کنند.

> ابرداده های آن را رسم کنید.

برای ترسیم ابرداده ها تابعی مانند زیر تعریف میکنیم:
```python
def print_metadata(image):
    has_metadata = False
    exifdata = image.getexif()
    for tag_id in exifdata:
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes
        if isinstance(data, bytes):
            has_metadata = True
            data = data.decode()
        print('   >>>',f"{tag:25}: {data}")
    return has_metadata
```
نکته‌ای که در این مورد لازم به ذکر میباشد این است که لزوما تمامی عکس ها دارای ابرداده نمیباشند. به عنوان مثال عکس پیش‌فرضی که در این گزارش استفاده شده است فاقد این اطلاعات است و معمولا عکس هایی ابرداده دارند که توسط دوربین گرفته شده اند. به عنوان مثال عکس زیر با دوربین موبایل گرفته شده است:
<img src="https://cdn.discordapp.com/attachments/732234196487241741/734420304050520104/3.jpg">
ین عکسی است که دارای ابرداده میباشد. بنابراین با فراخوانیِ تابع ساخته شده، اطلاعات مربوط به این عکس به صورت زیر نمایش داده خواهد شد(این عکس هم در پوشه ی فایل قرار دارد و با در آوردن خط کد مربوط به آن (خط ۱۲۶) از حالت کامنت قابل دسترسی است):
```python
>>> Q3: META DATAS :
   >>> ExifVersion              : 0220
   >>> ShutterSpeedValue        : (564, 100)
   >>> ApertureValue            : (252, 100)
   >>> DateTimeOriginal         : 2020:07:19 11:59:14
   >>> DateTimeDigitized        : 2020:07:19 11:59:14
   >>> BrightnessValue          : (282, 100)
   >>> ExposureBiasValue        : (0, 10)
   >>> MaxApertureValue         : (116, 100)
   >>> MeteringMode             : 3
   >>> Flash                    : 0
   >>> FlashPixVersion          : 0100
   >>> FocalLength              : (430, 100)
   >>> UserComment              :
   >>> ColorSpace               : 1
   >>> ComponentsConfiguration  : 
   >>> ExifImageWidth           : 4032
   >>> SubsecTime               : 0756
   >>> SubsecTimeOriginal       : 0756
   >>> SubsecTimeDigitized      : 0756
   >>> ExifImageHeight          : 1960
   >>> ImageLength              : 1960
   >>> Make                     : samsung
   >>> Model                    : SM-N960F
   >>> Orientation              : 1
   >>> YCbCrPositioning         : 1
   >>> ExposureTime             : (1, 50)
   >>> ExifInteroperabilityOffset: 815
   >>> XResolution              : (72, 1)
   >>> FNumber                  : (240, 100)
   >>> SceneType                : 
   >>> YResolution              : (72, 1)
   >>> ImageUniqueID            : J12LLKL00SM
   >>> ExposureProgram          : 2
   >>> CustomRendered           : 0
   >>> ISOSpeedRatings          : 100
   >>> ResolutionUnit           : 2
   >>> ExposureMode             : 0
   >>> ImageWidth               : 4032
   >>> WhiteBalance             : 0
   >>> Software                 : N960FXXU5ETF5
   >>> DateTime                 : 2020:07:19 11:59:14
   >>> DigitalZoomRatio         : (0, 0)
   >>> FocalLengthIn35mmFilm    : 26
   >>> SceneCaptureType         : 0
   >>> Contrast                 : 0
   >>> Saturation               : 0
   >>> Sharpness                : 0
   >>> ExifOffset               : 225

```
ولی در مورد عکس اصلی پیام عدم وجود ابرداده مشاهده خواهد شد.

 > میانگین داده ها را بیابید

با توجه به فرمول زیر میانگین را باید محاسبه کنیم و با کمک آن تابع زیر را تعریف میکنیم: 

M = (x1+...+xn)/(n) = (x1+...+x4000000)/(40000000)

```python
def calculate_mean(img):
    n = img.shape[0]
    mean =[[.0 , .0 , .0]]
    for pixel in range(img.shape[0]):
        mean = mean + img[pixel]
    mean = mean / n
    return mean
```
که خروجی این تابع  بردار میانگین خواهد بود.

> با استفاده از قسمت ۴ ، ماتریس کوواریانس را بسازید.

با رابطه ی داخل کتاب و همچنین داخل گزارش پروژه میتوان ماتریس کوواریانس را محاسبه کرد.
برای همین موضوع تابع زیر را تعریف میکنیم که عکس و میانگین را به عنوان آرگمان میگیرد و خروجی آن ماتریس کوواریانس خواهد بود:

```python
def calculate_covariance_matrix(img, m):
    n = img.shape[0]
    B = img
    for pixel in range(img.shape[0]):
        B[pixel] = B[pixel] - m
    B = B.transpose()
    s = (B.dot(B.transpose()))/(n-1)
    return s
```

> مقدار واریانس و همبستگی داده ها را محاسبه و بر اساس مقدار به دست آمده آن را تحلیل کنید.

با توجه به صفر بودن یا نبودن درایه های ماتریس کوواریانس تعیین میکنیم آیا وابستگی بین رنگ ها وجود دارد یا خیر. بعنوان مثال:

```python
>>> Q6: COVARIANCE MATRIX ANALYSIS:
   >>> COVARIANCES ANALYSIS:
      >>> COV( X 1 , X 2 )= 0.0         ->      X 1 and X 2 are UNCORRELATED.
      >>> COV( X 1 , X 3 )= 0.0         ->      X 1 and X 3 are UNCORRELATED.
      >>> COV( X 2 , X 1 )= 0.0         ->      X 2 and X 1 are UNCORRELATED.
      >>> COV( X 2 , X 3 )= 0.0001
      >>> COV( X 3 , X 1 )= 0.0         ->      X 3 and X 1 are UNCORRELATED.
      >>> COV( X 3 , X 2 )= 0.0001
   >>> VARIANCES ANALYSIS:
      >>> VAR( X 1 )= 0.0
      >>> VAR( X 2 )= 0.0
      >>> VAR( X 3 )= 0.0001
```

> داده ای که در حال حاضر با آن کار میکنید 3 بعدی است. آیا بعد آن را میتوان کاهش داد؟ برای این
منظور از روش واریانس کل داده ها استفاده کنید
 
 واریانس کل را محاسبه میکنیم و مقادیر ویژه را بر آن تقسیم میکنیم:
 ```python
 def calculate_total_variance(variance_matrix):
    total_variance = .0
    for v in range(3):
        total_variance = total_variance + variance_matrix[0][v]
    return round(total_variance,2)
```


> با استفاده از روش analyze component principle حداقل یک عکس جدید از ورودی خود
تولید کنید 


<img src="https://cdn.discordapp.com/attachments/732234196487241741/734420313865191524/4.jpg">
