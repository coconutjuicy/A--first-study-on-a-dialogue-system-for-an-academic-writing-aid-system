# dialogue-system

![Ni_Zihui_final_presentation_01](https://user-images.githubusercontent.com/40939276/158305556-8322d050-c98c-419a-b431-adc850cc8ad3.jpg)

![Ni_Zihui_final_presentation_04](https://user-images.githubusercontent.com/40939276/158305583-05264c10-ed6b-4399-9dc0-64fb9720c241.jpg)

![Ni_Zihui_final_presentation_05](https://user-images.githubusercontent.com/40939276/158305603-d5c36c85-69c8-4557-84f2-dd7dd9c997c2.jpg)

![Ni_Zihui_final_presentation_06](https://user-images.githubusercontent.com/40939276/158305621-3082028b-b6bc-4ed3-89d2-47d156f511b2.jpg)

![Ni_Zihui_final_presentation_19](https://user-images.githubusercontent.com/40939276/158305681-b705133f-3353-4ffd-a3f0-3498e8166f4d.jpg)



![Ni_Zihui_final_presentation_20](https://user-images.githubusercontent.com/40939276/158305692-f5c1be8c-9550-498c-8f3a-8f8f53907c12.jpg)

まずactをdstc 2データセットから抽出する手順はextract_act.pyにある.

actを抽出するとslotを認識しslotを修正することができる.このステップの操作はchange_slot.pyに書かれています。

![Ni_Zihui_final_presentation_21](https://user-images.githubusercontent.com/40939276/158305877-884867a6-6e40-41f1-8454-eabf2b5846f7.jpg)

![Ni_Zihui_final_presentation_23](https://user-images.githubusercontent.com/40939276/158306273-c5ac5b56-2c27-4054-b498-68d878398395.jpg)

BERTモデルを用いて重要な単語を置換する操作はLM_final.pyで行う.

![Ni_Zihui_final_presentation_24](https://user-images.githubusercontent.com/40939276/158306395-a9c673aa-322a-441b-952d-821cd046f5a3.jpg)


![Ni_Zihui_final_presentation_27](https://user-images.githubusercontent.com/40939276/158306434-60ae8c06-1684-498c-a71f-a2ce464635e8.jpg)

![Ni_Zihui_final_presentation_29](https://user-images.githubusercontent.com/40939276/158306481-1d046f35-51a6-4f33-bd75-bfc9cd8b1226.jpg)

これは私たちのデータセットの修正の結果です。結果はこれらのdstc2-trn.jsonlist、dstc2-tst.jsonlist、dstc2-val.jsonlistに書いてありました。


![Ni_Zihui_final_presentation_31](https://user-images.githubusercontent.com/40939276/158306755-b4eb6d03-f894-4e35-baaa-dc9a353ae4ee.jpg)

これは私たちの実験結果です。実験データにより、対話システムを修正したデータセットに移行することに成功しました。

