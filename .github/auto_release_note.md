这是定期自动生成的 Release，如果发现问题请提 issue 并暂时选择到 [此处](https://github.com/ZingLix/immich-geodata-cn/releases) 选择手动发布的 Release 文件。

如果遇到 Immich 没有更新数据，请手动修改 geodata-date.txt 文件，将其内容中的时间修改为更新的时间（比如当前时间）。

**BETA** 提供了多种展示地名的级别，可根据需要选择对应的文件。

> [!IMPORTANT]  
> 每个 release 中的更新时间都是相同的，这意味着如果更换同一个 release 中的不同版本文件，Immich 无法检测到数据更新。
>
> 因此，如果想要尝试同个 release 下不同的数据文件，请手动调整解压后的 geodata-date.txt 文件，将其内容中的时间修改为更靠后的时间（比如当前时间），并在 Immich 启动时观察是否有 `10000 geodata records imported` 日志出现，从而确定是否成功更新了数据文件。

以 `中国,江苏省,苏州市,昆山市,周市镇` 为例

|示例|对应文件|数据增强<br>数据更多、定位更准但编码更慢|
|:---|:---|:---|
|苏州市|geodata.zip<br>geodata_admin_2.zip|geodata_full.zip<br>geodata_admin_2_full.zip|
|昆山市|geodata_admin_3.zip|geodata_admin_3_full.zip|
|周市镇|geodata_admin_4.zip|geodata_admin_4_full.zip|
|苏州市 昆山市|geodata_admin_2_admin_3.zip|geodata_admin_2_admin_3_full.zip|
|苏州市 周市镇|geodata_admin_2_admin_4.zip|geodata_admin_2_admin_4_full.zip|
|昆山市 周市镇|geodata_admin_3_admin_4.zip|geodata_admin_3_admin_4_full.zip|
|苏州市 昆山市 周市镇|geodata_admin_2_admin_3_admin_4.zip|geodata_admin_2_admin_3_admin_4_full.zip|

> [!WARNING]  
> 受限于 Immich 自身反向地理编码原理，在接近边界时识别效果不佳，而使用级别更低的数据时更容易遇到边界问题，因此更容易导致识别错误，请注意
>
> 如果遇到该情况，可以尝试使用数据增强版本的数据，或者在 [GeoNames](https://www.geonames.org/) 提交相关位置的数据