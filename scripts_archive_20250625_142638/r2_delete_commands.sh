#!/bin/bash
# R2图片清理脚本
# 生成时间: 2025-06-24 21:00:08
# 删除 106 张无标签图片

echo "🧹 开始清理R2存储桶..."
echo "将删除 106 张无标签图片"
echo ""

# R2配置
R2_BUCKET="thinkora-pics"
R2_ENDPOINT="https://d37e2728a4daeb263e7a08a066e80926.r2.cloudflarestorage.com"

# 统计变量
DELETED=0
FAILED=0

# 删除函数
delete_file() {
    local file_path=$1
    echo -n "删除: $file_path ... "
    
    # 使用aws cli或rclone删除
    # 选项1: 使用aws cli
    # aws s3 rm "s3://$R2_BUCKET/$file_path" --endpoint-url="$R2_ENDPOINT"
    
    # 选项2: 使用rclone（需要配置）
    # rclone delete "r2:$R2_BUCKET/$file_path"
    
    # 选项3: 使用curl（需要签名，较复杂）
    echo "[需要配置删除命令]"
}

# 删除旧图片

# 删除 10727328
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}10727328.${ext}"
    done
done

# 删除 8516791
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}8516791.${ext}"
    done
done

# 删除 8532777
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}8532777.${ext}"
    done
done

# 删除 GZUwekngRYM
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}GZUwekngRYM.${ext}"
    done
done

# 删除 mQ9vzpnjYnA
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}mQ9vzpnjYnA.${ext}"
    done
done

# 删除 uh_W-27b8Lw
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}uh_W-27b8Lw.${ext}"
    done
done

# 删除 unsplash_-lkFmMG1BP0
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_-lkFmMG1BP0.${ext}"
    done
done

# 删除 unsplash_0V3uVjouHRc
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_0V3uVjouHRc.${ext}"
    done
done

# 删除 unsplash_0o6Lqin4nNE
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_0o6Lqin4nNE.${ext}"
    done
done

# 删除 unsplash_0tpQf53l_Sg
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_0tpQf53l_Sg.${ext}"
    done
done

# 删除 unsplash_1SAnrIxw5OY
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_1SAnrIxw5OY.${ext}"
    done
done

# 删除 unsplash_3IA4-tUDyKI
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_3IA4-tUDyKI.${ext}"
    done
done

# 删除 unsplash_5EgJ-mUklbg
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_5EgJ-mUklbg.${ext}"
    done
done

# 删除 unsplash_5dN0V94g4s4
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_5dN0V94g4s4.${ext}"
    done
done

# 删除 unsplash_6PF6DaiWz48
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_6PF6DaiWz48.${ext}"
    done
done

# 删除 unsplash_6VeIwIf3c_g
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_6VeIwIf3c_g.${ext}"
    done
done

# 删除 unsplash_8krX0HkXw8c
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_8krX0HkXw8c.${ext}"
    done
done

# 删除 unsplash_9C-lLIVLM4o
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_9C-lLIVLM4o.${ext}"
    done
done

# 删除 unsplash_A-aj4HQTy7M
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_A-aj4HQTy7M.${ext}"
    done
done

# 删除 unsplash_Ajhnl1IW-ws
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_Ajhnl1IW-ws.${ext}"
    done
done

# 删除 unsplash_BOHeLl3wR5o
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_BOHeLl3wR5o.${ext}"
    done
done

# 删除 unsplash_CmF_5GYc6c0
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_CmF_5GYc6c0.${ext}"
    done
done

# 删除 unsplash_D6vNidzLIGE
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_D6vNidzLIGE.${ext}"
    done
done

# 删除 unsplash_DDBO05yBbuk
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_DDBO05yBbuk.${ext}"
    done
done

# 删除 unsplash_DJ7bWa-Gwks
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_DJ7bWa-Gwks.${ext}"
    done
done

# 删除 unsplash_DfRRllois_I
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_DfRRllois_I.${ext}"
    done
done

# 删除 unsplash_DvtuUqi6T7Y
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_DvtuUqi6T7Y.${ext}"
    done
done

# 删除 unsplash_EUcrDD6Rgng
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_EUcrDD6Rgng.${ext}"
    done
done

# 删除 unsplash_EZSm8xRjnX0
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_EZSm8xRjnX0.${ext}"
    done
done

# 删除 unsplash_FHnnjk1Yj7Y
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_FHnnjk1Yj7Y.${ext}"
    done
done

# 删除 unsplash_FaPxZ88yZrw
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_FaPxZ88yZrw.${ext}"
    done
done

# 删除 unsplash_Gj9MaaTzGZ0
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_Gj9MaaTzGZ0.${ext}"
    done
done

# 删除 unsplash_GnvurwJsKaY
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_GnvurwJsKaY.${ext}"
    done
done

# 删除 unsplash_HY3l4IeOc3E
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_HY3l4IeOc3E.${ext}"
    done
done

# 删除 unsplash_Hj8paHW1pZ4
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_Hj8paHW1pZ4.${ext}"
    done
done

# 删除 unsplash_I01NQ8W1hQY
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_I01NQ8W1hQY.${ext}"
    done
done

# 删除 unsplash_JRiJXnPlctg
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_JRiJXnPlctg.${ext}"
    done
done

# 删除 unsplash_K9PXRiSArJA
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_K9PXRiSArJA.${ext}"
    done
done

# 删除 unsplash_KOgh9vct6ng
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_KOgh9vct6ng.${ext}"
    done
done

# 删除 unsplash_NsWcRlBT_74
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_NsWcRlBT_74.${ext}"
    done
done

# 删除 unsplash_OYMKjv5zmGU
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_OYMKjv5zmGU.${ext}"
    done
done

# 删除 unsplash_PM4Vu1B0gxk
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_PM4Vu1B0gxk.${ext}"
    done
done

# 删除 unsplash_Q8My8QEsvY8
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_Q8My8QEsvY8.${ext}"
    done
done

# 删除 unsplash_QLqNalPe0RA
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_QLqNalPe0RA.${ext}"
    done
done

# 删除 unsplash_QeVmJxZOv3k
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_QeVmJxZOv3k.${ext}"
    done
done

# 删除 unsplash_RxuIPn5UiBE
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_RxuIPn5UiBE.${ext}"
    done
done

# 删除 unsplash_SqLyNHbsLKQ
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_SqLyNHbsLKQ.${ext}"
    done
done

# 删除 unsplash_U0tBTn8UR8I
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_U0tBTn8UR8I.${ext}"
    done
done

# 删除 unsplash_U7aeXmoaVH0
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_U7aeXmoaVH0.${ext}"
    done
done

# 删除 unsplash_URBF9cjd4S8
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_URBF9cjd4S8.${ext}"
    done
done

# 删除 unsplash_UtzrcidfCsk
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_UtzrcidfCsk.${ext}"
    done
done

# 删除 unsplash_VieM9BdZKFo
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_VieM9BdZKFo.${ext}"
    done
done

# 删除 unsplash_XMFZqrGyV-Q
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_XMFZqrGyV-Q.${ext}"
    done
done

# 删除 unsplash_XUc3vxLzznE
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_XUc3vxLzznE.${ext}"
    done
done

# 删除 unsplash_XXpbdU_31Sg
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_XXpbdU_31Sg.${ext}"
    done
done

# 删除 unsplash_Yd2Pcn0plNU
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_Yd2Pcn0plNU.${ext}"
    done
done

# 删除 unsplash_Z9FzzMQVCeM
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_Z9FzzMQVCeM.${ext}"
    done
done

# 删除 unsplash_ZLeogVvtXk0
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_ZLeogVvtXk0.${ext}"
    done
done

# 删除 unsplash__SkAipDtFJU
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash__SkAipDtFJU.${ext}"
    done
done

# 删除 unsplash__lhefRJtT0U
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash__lhefRJtT0U.${ext}"
    done
done

# 删除 unsplash__sg8nXmpWDM
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash__sg8nXmpWDM.${ext}"
    done
done

# 删除 unsplash_aD6mY43V_QQ
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_aD6mY43V_QQ.${ext}"
    done
done

# 删除 unsplash_aOC7TSLb1o8
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_aOC7TSLb1o8.${ext}"
    done
done

# 删除 unsplash_aq86sStVYDg
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_aq86sStVYDg.${ext}"
    done
done

# 删除 unsplash_bKjHgo_Lbpo
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_bKjHgo_Lbpo.${ext}"
    done
done

# 删除 unsplash_cGcB2-6Y6vs
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_cGcB2-6Y6vs.${ext}"
    done
done

# 删除 unsplash_cbRZ8p2hT58
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_cbRZ8p2hT58.${ext}"
    done
done

# 删除 unsplash_cckf4TsHAuw
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_cckf4TsHAuw.${ext}"
    done
done

# 删除 unsplash_d1ngW7SNehM
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_d1ngW7SNehM.${ext}"
    done
done

# 删除 unsplash_dVAeys3iwV0
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_dVAeys3iwV0.${ext}"
    done
done

# 删除 unsplash_eQptGspn0YU
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_eQptGspn0YU.${ext}"
    done
done

# 删除 unsplash_fMD_Cru6OTk
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_fMD_Cru6OTk.${ext}"
    done
done

# 删除 unsplash_hR_igpGNuxA
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_hR_igpGNuxA.${ext}"
    done
done

# 删除 unsplash_iSeawjCwtLs
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_iSeawjCwtLs.${ext}"
    done
done

# 删除 unsplash_iiUAdB0UfXo
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_iiUAdB0UfXo.${ext}"
    done
done

# 删除 unsplash_jLwVAUtLOAQ
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_jLwVAUtLOAQ.${ext}"
    done
done

# 删除 unsplash_jVaQjaQA4aw
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_jVaQjaQA4aw.${ext}"
    done
done

# 删除 unsplash_jb10hnn2JVs
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_jb10hnn2JVs.${ext}"
    done
done

# 删除 unsplash_jiVeo0i1EB4
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_jiVeo0i1EB4.${ext}"
    done
done

# 删除 unsplash_kn58STigDRc
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_kn58STigDRc.${ext}"
    done
done

# 删除 unsplash_kw0z6RyvC0s
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_kw0z6RyvC0s.${ext}"
    done
done

# 删除 unsplash_mnPYsp7eJ44
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_mnPYsp7eJ44.${ext}"
    done
done

# 删除 unsplash_o-7o3lkShsg
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_o-7o3lkShsg.${ext}"
    done
done

# 删除 unsplash_oy9c7o_yeD0
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_oy9c7o_yeD0.${ext}"
    done
done

# 删除 unsplash_p1acECGO3z0
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_p1acECGO3z0.${ext}"
    done
done

# 删除 unsplash_pVt9j3iWtPM
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_pVt9j3iWtPM.${ext}"
    done
done

# 删除 unsplash_pY1lV9kHSn0
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_pY1lV9kHSn0.${ext}"
    done
done

# 删除 unsplash_q10VITrVYUM
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_q10VITrVYUM.${ext}"
    done
done

# 删除 unsplash_qr2cn19ixQs
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_qr2cn19ixQs.${ext}"
    done
done

# 删除 unsplash_rQb-17JmGmk
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_rQb-17JmGmk.${ext}"
    done
done

# 删除 unsplash_s9CC2SKySJM
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_s9CC2SKySJM.${ext}"
    done
done

# 删除 unsplash_tBY1-5dKj1s
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_tBY1-5dKj1s.${ext}"
    done
done

# 删除 unsplash_ttNhljJAtdI
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_ttNhljJAtdI.${ext}"
    done
done

# 删除 unsplash_u3ajSXhZM_U
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_u3ajSXhZM_U.${ext}"
    done
done

# 删除 unsplash_u8tvMIguCiM
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_u8tvMIguCiM.${ext}"
    done
done

# 删除 unsplash_ute2XAFQU2I
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_ute2XAFQU2I.${ext}"
    done
done

# 删除 unsplash_v-7RPus9LDw
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_v-7RPus9LDw.${ext}"
    done
done

# 删除 unsplash_vMMnyZ2lAmw
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_vMMnyZ2lAmw.${ext}"
    done
done

# 删除 unsplash_vfiuGpL9fiU
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_vfiuGpL9fiU.${ext}"
    done
done

# 删除 unsplash_vhpD1Ikatwo
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_vhpD1Ikatwo.${ext}"
    done
done

# 删除 unsplash_w2KaSI3IvPM
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_w2KaSI3IvPM.${ext}"
    done
done

# 删除 unsplash_wVjIu15NGBs
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_wVjIu15NGBs.${ext}"
    done
done

# 删除 unsplash_xcI7f25UQSs
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_xcI7f25UQSs.${ext}"
    done
done

# 删除 unsplash_xxeAftHHq6E
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_xxeAftHHq6E.${ext}"
    done
done

# 删除 unsplash_ylveRpZ8L1s
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_ylveRpZ8L1s.${ext}"
    done
done

# 删除 unsplash_zw8t5aMmJQQ
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${prefix}unsplash_zw8t5aMmJQQ.${ext}"
    done
done

echo ""
echo "✅ 清理完成!"
echo "   成功删除: $DELETED 个文件"
echo "   删除失败: $FAILED 个文件"
