template <class ResUnit, class KeyType>
bool ResLoader<ResUnit, KeyType>::Load(const std::string& file_name)
{
    // 原来的配置表导出太复杂加上有部分工具缺失，现在用python重写导出bin文件的工具
    // 相应的bin文件的load方法也要重写
    // 2016年12月19日09:40:23
	std::string res_path = Herm::GetModulePath();
	res_path += file_name;
	std::ifstream file(res_path.c_str(), std::ios_base::in | std::ios_base::binary);
	if (!file)
	{
        HERM_ERROR("open %s failed!", file_name.c_str());
		return false;
	}

    // 读取python脚本pack的大小
	file.seekg(0);
	Herm::uint32_t python_pack_size;
	file.read((char*)&python_pack_size, sizeof(python_pack_size));
	if (python_pack_size != sizeof(ResUnit))
	{
        HERM_ERROR("[%s] python pack size(%d) != cpp struct size(%d)", file_name.c_str(), python_pack_size, sizeof(ResUnit) );
		return false;
	}

    // 读取行数
	file.seekg(4);
	Herm::uint32_t count;
	file.read((char*)&count, sizeof(count));
	m_count = (int)count;

	// Reload()的时候保证把旧的资源数据清理掉
	OnClear();

    // 读取配置
	file.seekg(8);
	for (Herm::uint32_t i = 0; i < count; i++)
	{
		ResUnit metaUnit; 
		file.read((char*)&metaUnit, sizeof(metaUnit));

		if (!OnGetUnit(metaUnit))
			return false;
	}

	return true;
}
