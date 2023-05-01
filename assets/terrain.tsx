<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.10.1" name="terrain" tilewidth="32" tileheight="32" tilecount="180" columns="10">
 <image source="tile1.png" width="320" height="320"/>
 <tile id="3">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0.363636" y="1.63636" width="31.6364" height="30.3636"/>
  </objectgroup>
 </tile>
 <tile id="4">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0" width="30.1818" height="31.6364"/>
  </objectgroup>
 </tile>
 <tile id="12">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0.363636" y="0" width="31.6364" height="29.4545"/>
  </objectgroup>
 </tile>
 <tile id="13">
  <objectgroup draworder="index" id="2">
   <object id="1" x="4.18182" y="-0.181818" width="27.8182" height="32"/>
  </objectgroup>
 </tile>
 <tile id="14">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0.181818" y="2" width="29.0909" height="29.2727"/>
  </objectgroup>
 </tile>
 <tile id="22">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0.181818" y="0" width="29.2727" height="28.9091"/>
  </objectgroup>
 </tile>
 <tile id="23">
  <objectgroup draworder="index" id="2">
   <object id="1" x="3.09091" y="0.363636" width="28.9091" height="29.0909"/>
  </objectgroup>
 </tile>
 <tile id="24">
  <objectgroup draworder="index" id="3">
   <object id="4" x="2.36364" y="1.63636" width="29.4545" height="30"/>
  </objectgroup>
 </tile>
 <wangsets>
  <wangset name="grass" type="mixed" tile="-1">
   <wangcolor name="" color="#ff0000" tile="2" probability="1"/>
   <wangtile tileid="2" wangid="1,1,1,1,1,1,1,1"/>
   <wangtile tileid="3" wangid="0,0,1,1,1,1,1,0"/>
   <wangtile tileid="4" wangid="1,0,0,0,1,1,1,1"/>
   <wangtile tileid="12" wangid="1,1,1,0,0,0,1,1"/>
   <wangtile tileid="13" wangid="1,1,1,1,1,0,0,0"/>
   <wangtile tileid="14" wangid="0,0,0,0,1,1,1,0"/>
   <wangtile tileid="22" wangid="1,0,0,0,0,0,1,1"/>
   <wangtile tileid="23" wangid="1,1,1,0,0,0,0,0"/>
   <wangtile tileid="24" wangid="0,0,1,1,1,0,0,0"/>
   <wangtile tileid="32" wangid="1,0,1,1,1,1,1,1"/>
   <wangtile tileid="33" wangid="1,1,1,0,1,1,1,1"/>
   <wangtile tileid="34" wangid="1,1,1,1,1,0,1,1"/>
   <wangtile tileid="42" wangid="1,1,1,1,1,1,1,0"/>
  </wangset>
 </wangsets>
</tileset>
