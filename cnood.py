import os
import csv
import re


def farsi_to_fingilish(text):
    mapping = {
        "آ": "A", "ا": "A", "ب": "B", "پ": "P", "ت": "T", "ث": "S", "ج": "J", "چ": "Ch",
        "ح": "H", "خ": "Kh", "د": "D", "ذ": "Z", "ر": "R", "ز": "Z", "ژ": "Zh", "س": "S",
        "ش": "Sh", "ص": "S", "ض": "Z", "ط": "T", "ظ": "Z", "ع": "A", "غ": "Gh", "ف": "F",
        "ق": "Gh", "ک": "K", "گ": "G", "ل": "L", "م": "M", "ن": "N", "و": "V", "ه": "H", "ی": "I","ي":"I",
        "ك":"K","ئ":"I"
    }

    result = "".join(mapping.get(char, char) for char in text)
    return result

def extract_data_from_filenames(root_folder):
    ostan_names={'11 \u202bاستان تهران\u202c': '11 Tehran', '14 \u202bاستان قم\u202c': '14 Qom', '15 \u202bاستان قزوين\u202c': '15 Qazvin', '16 \u202bاستان مازندران\u202c': '16 Mazandaran', '18 \u202bاستان البرز\u202c': '18 Alborz', '21 \u202bاستان اصفهان\u202c': '21 Esfahan', '26 \u202bاستان آذربايجان شرقي\u202c': '26 AzarbayjanSharghi', '31 \u202bاستان خراسان رضوي\u202c': '31 KhorasanRazavi', '32 \u202bاستان خراسان شمالي\u202c': '32 KhorasanShomali', '33 \u202bاستان خراسان جنوبي\u202c': '33 KhorasanJonoubi', '36 \u202bاستان خوزستان \u202c': '36 Khuzestan', '41 \u202bاستان فارس\u202c': '41 Fars', '45 \u202bاستان کرمان \u202c': '45 Kerman', '51 \u202bاستان مرکزي\u202c': '51 Markazi', '54 \u202bاستان گيلان\u202c': '54 Gilan', '57 \u202bاستان آذربايجان غربي\u202c': '57 AzarbayjanGharbi', '61 \u202bاستان سيستان و بلوچستان\u202c': '61 SistanAndBaluchestan', '64 \u202bاستان هرمزگان\u202c': '64 Hormozgan', '67 \u202bاستان زنجان\u202c': '67 Zanjan', '71 \u202bاستان کرمانشاه\u202c': '71 KermanShah', '73 \u202bاستان کردستان\u202c': '73 Kurdistan', '75 \u202bاستان همدان\u202c': '75 Hamedan', '77 \u202bاستان چهارمحال و بختياري\u202c': '77 ChaharmahalAndBakhtiari', '81 \u202bاستان لرستان\u202c': '81 Lorestan', '83 \u202bاستان ايلام\u202c': '83 ilam', '85 \u202bاستان کهگيلويه و بويراحمد\u202c': '85 KohgiluyeAndBoyerahmad', '87 \u202bاستان سمنان\u202c': '87 Semnan', '91 \u202bاستان اردبيل\u202c': '91 Ardabil', '93 \u202bاستان يزد\u202c': '93 Yazd', '95 \u202bاستان بوشهر\u202c': '95 Bushehr', '97 \u202bاستان گلستان\u202c': '97 Golestan'}

    cleaned_data = []
    special_cases=[]
    count=0
    for ostan in os.listdir(root_folder):

        ostan_path = os.path.join(root_folder, ostan, "Daily Data")
        if not os.path.exists(ostan_path):
            ostan_path = os.path.join(root_folder, ostan, "‫حجم تردد روزانه‬")

        


        for filename in os.listdir(ostan_path):
            count=count+1





            match = re.match(r"Daily\s*(\d{6,7})\s*(.+)\.xlsx", filename)

            if match:


                code_mehvar = match.group(1)
                name_mehvar = match.group(2).replace(".xlsx", "").strip()

                #remove (somthing) in name_mehvar
                name_mehvar_edited = re.sub(r"\s*\(.*?\)", "", name_mehvar).strip()







                if "-" in name_mehvar_edited:
                    if "،" in name_mehvar_edited:

                        special_cases.append(filename)
                        continue
                    if "قطعه اول آزادراه"in name_mehvar_edited:
                        name_mehvar_edited = name_mehvar_edited.replace("قطعه اول آزادراه", "")
                    if "خروجي آزادراه"in name_mehvar_edited:
                        name_mehvar_edited = name_mehvar_edited.replace("خروجي آزادراه", "")
                    if "تقاطع"in name_mehvar_edited:
                        name_mehvar_edited = name_mehvar_edited.replace("تقاطع", "")
                    if "پليس راه"in name_mehvar_edited:
                        name_mehvar_edited = name_mehvar_edited.replace("پليس راه", "")
                    if "آزادراه"in name_mehvar_edited:
                        name_mehvar_edited = name_mehvar_edited.replace("آزادراه", "")
                    if "آزاد راه"in name_mehvar_edited:
                        name_mehvar_edited = name_mehvar_edited.replace("آزاد راه", "")

                    if  "کنار گذر" in name_mehvar_edited:
                        name_mehvar_edited = name_mehvar_edited.replace("کنار گذر", "")
                    if  "کنارگذر" in name_mehvar_edited:
                        name_mehvar_edited = name_mehvar_edited.replace("کنارگذر", "")
                    if "عوارضي" in name_mehvar_edited:
                        name_mehvar_edited=name_mehvar_edited.replace("عوارضي","")
                    if "گيت" in name_mehvar_edited:

                        name_mehvar_edited=name_mehvar_edited.replace("مجموع گيت هاي","")

                    if "سه راهي" in name_mehvar_edited:
                        name_mehvar_edited = name_mehvar_edited.replace("سه راهي", "")
                    if "جاده قديم" in name_mehvar_edited:
                        name_mehvar_edited = name_mehvar_edited.replace("جاده قديم", "")



                    if "جاده مخصوص" in name_mehvar_edited:
                        name_mehvar_edited = name_mehvar_edited.replace("جاده مخصوص", "")

                    if "سه راه" in name_mehvar_edited:
                        name_mehvar_edited = name_mehvar_edited.replace("سه راه", "")
                    if "سه‌راهي" in name_mehvar_edited:
                        name_mehvar_edited = name_mehvar_edited.replace("سه‌راهي", "")
                    if "سه‌راه" in name_mehvar_edited:
                        name_mehvar_edited = name_mehvar_edited.replace("سه‌راه", "")
                    if "کمربندي شرقي" in name_mehvar_edited:
                        name_mehvar_edited = name_mehvar_edited.replace("کمربندي شرقي", "")
                    if "کمربندي غربي" in name_mehvar_edited:
                        name_mehvar_edited = name_mehvar_edited.replace("کمربندي غربي", "")
                    if "کمربندي" in name_mehvar_edited:
                        name_mehvar_edited = name_mehvar_edited.replace("کمربندي", "")
                    if "محور قديم" in name_mehvar_edited:
                        name_mehvar_edited = name_mehvar_edited.replace("محور قديم", "")

                    if "پل جاده" in name_mehvar_edited:
                        name_mehvar_edited = name_mehvar_edited.replace("پل جاده", "")


                    if "جاده" in name_mehvar_edited:
                        name_mehvar_edited = name_mehvar_edited.replace("جاده", "")
                    if "بزرگراه" in name_mehvar_edited:
                        name_mehvar_edited = name_mehvar_edited.replace("‫بزرگراه", "")

                    if  "(دو راهي جبرآباد" in name_mehvar_edited:
                        name_mehvar_edited=name_mehvar_edited.replace("(دو راهي جبرآباد", "")

                    if  "دو راهي" in name_mehvar_edited:
                        name_mehvar_edited=name_mehvar_edited.replace("دو راهي", "")
                    if  "دوراهي" in name_mehvar_edited:
                        name_mehvar_edited=name_mehvar_edited.replace("دوراهي", "")
                    if  "ميدان سلفچگان" in name_mehvar_edited:
                        name_mehvar_edited=name_mehvar_edited.replace("میدان", "")
                    if  "ي" in name_mehvar_edited:
                        name_mehvar_edited=name_mehvar_edited.replace("ي", "ی")






                    origin, destination = name_mehvar_edited.split("-", 1)
                    origin=origin.strip()
                    destination=destination.strip()
                    origin=origin.replace(" ", "")
                    destination=destination.replace(" ", "")
                    origin=origin.replace("‌", "")
                    destination=destination.replace("‌", "")
                    orgin_en = farsi_to_fingilish(origin)
                    destination_en = farsi_to_fingilish(destination)

                    if ostan  in ostan_names:
                        ostan=ostan_names[ostan]


                    cleaned_data.append([code_mehvar, name_mehvar, ostan, origin.strip(), destination.strip(),orgin_en,destination_en,filename.replace(".xlsx", "")])











                else:
                    special_cases.append(filename)
                

    return (cleaned_data, special_cases)



root_directory = "C:\\Users\\Moham\\OneDrive\\Desktop\\all0"


root_directory1="C:\\Users\\Moham\\OneDrive\\Desktop\\all"
root_directory2="C:\\Users\\Moham\\OneDrive\\Desktop\\all2\\all2"
root_directory3="C:\\Users\\Moham\\OneDrive\\Desktop\\all3"
root_directory4="C:\\Users\\Moham\\OneDrive\\Desktop\\all4"
directories=[root_directory1,root_directory3,root_directory4]
output_file = "output.csv"
n1,s1=extract_data_from_filenames(root_directory)

for directory in directories:
    n,s=extract_data_from_filenames(directory)
    for b in n :
        count_for_code_mehvar=0
        for a in n1:
            if b[0]==a[0]:
                count_for_code_mehvar=count_for_code_mehvar+1



        if count_for_code_mehvar==0:
            n1.append(b)

    for f in s:
        if f not in s1:
            s1.append(f)

with open(output_file, "w", newline="", encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Code-mehvar", "Name-Mehvar", "Ostan", "origin", "destination","orgin_en","destination_en","filename"])
    writer.writerows(n1)

with open("my_file.txt", "w", encoding="utf-8") as file:
    for item in s1:
        file.write(item + "\n")