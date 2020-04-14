#!/bin/bash -e

pickle_dir="$HOME/inaho_robo/output/aspara_detector/recognition"
config_dir="$HOME/inaho_robo/config/aspara_detector"
tmp_dir="/tmp/copy_pickle_log/$(date '+%Y-%m-%d')/pickle"


echo "pickleデータとzense設定ファイルのコピーを行います"

mkdir -pv $tmp_dir
cp -rv $pickle_dir/* $tmp_dir
cp -v $config_dir/*.toml $tmp_dir

cat << EOS > $tmp_dir/README.md
圃場          ：xx
ハウス番号    ：xx
ロボ          ：P3-#xx
ロボ運用担当者：xx
撮影時間      ：xx時 - xx時
天候          ：xx ［晴れ | 曇り | 雨］
EOS

echo "コピーが完了しました"
echo ""
echo "次のファイルのxxに各種情報を記載してね (・ω<)"
echo $tmp_dir/README.md

