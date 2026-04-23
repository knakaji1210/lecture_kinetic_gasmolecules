# lecture_kinetic_gasmolecules

講義「分子運動論」で利用するために、Googleに頼んで作ってもらったもの。中身を精査していない。  

以下、Googleからのコメント  

gas_molecules_no_collision.py  
速度の分布を正規分布で作成  
2Dではレイリー分布に  

gas_molecules_collision.py  
衝突判定  
全ペアの距離を計算し、距離d < 2*rなら衝突とみなす。  
衝突した瞬間に、中心を結ぶ線方向の成分を入れ替え  
粒子がめり込んで動けなくなるのを防ぐため、衝突直後に位置を少し離す処理  
