import json

class AlchemyRecipeDecoder:
    """炼金配方解码器，将JSON格式转换为配方数据"""
    
    def decode(self, json_string):
        """
        将JSON字符串解码为配方数据
        
        参数:
            json_string: JSON格式的字符串
        
        返回:
            包含配方信息的字典
        """
        try:
            recipe_data = json.loads(json_string)
        except json.JSONDecodeError as e:
            raise ValueError(f"无效的JSON格式: {str(e)}")
        
        # 验证必要的字段
        required_fields = ['id', 'name', 'tags', 'materials', 'base_elements', 'rewards']
        for field in required_fields:
            if field not in recipe_data:
                raise ValueError(f"JSON缺少必要的字段: {field}")
        
        # 验证材料字段
        if not isinstance(recipe_data['materials'], list):
            raise ValueError("材料字段必须是列表")
        
        for i, material in enumerate(recipe_data['materials']):
            if 'type' not in material or 'id' not in material:
                raise ValueError(f"材料 {i+1} 必须包含 'type' 和 'id'")
        
        # 验证基本炼金成分字段
        if not isinstance(recipe_data['base_elements'], list):
            raise ValueError("基本炼金成分字段必须是列表")
        
        for i, element in enumerate(recipe_data['base_elements']):
            if 'id' not in element:
                raise ValueError(f"基本炼金成分 {i+1} 必须包含 'id'")
            
            # 验证网格编码
            try:
                grid_state, color = RewardGridDecoder().decode(element['id'])
                if not color:
                    raise ValueError(f"基本炼金成分 {i+1} 必须指定元素属性")
            except ValueError as e:
                raise ValueError(f"基本炼金成分 {i+1} 的网格编码无效: {str(e)}")
        
        # 验证奖励字段
        for i, reward in enumerate(recipe_data['rewards']):
            if 'level' not in reward or 'property' not in reward or 'id' not in reward:
                raise ValueError(f"奖励 {i+1} 缺少必要的字段")
            
            # 验证网格编码
            try:
                grid_state, color = RewardGridDecoder().decode(reward['id'])
                if not color:
                    raise ValueError(f"奖励 {i+1} 必须指定元素属性")
            except ValueError as e:
                raise ValueError(f"奖励 {i+1} 的网格编码无效: {str(e)}")
        
        return recipe_data


class RewardGridDecoder:
    """奖励网格解码器，将ID字符串解码为3x3网格状态"""
    
    def decode(self, encoded_id):
        """
        将ID字符串解码为3x3网格状态
        
        参数:
            encoded_id: 编码后的ID字符串
        
        返回:
            (grid_state, color): 网格状态列表和颜色（颜色应用于非空白格子）
        """
        # 检查是否包含颜色信息
        color = None
        if ":" not in encoded_id:
            raise ValueError("缺少元素属性")
        
        encoded_id, color_code = encoded_id.split(":")
        color_map = {
            "R": "火系",
            "B": "水系",
            "G": "草系",
            "Y": "雷系"
        }
        color = color_map.get(color_code)
        if not color:
            raise ValueError("无效的元素属性")
        
        # 验证编码长度
        if len(encoded_id) != 9:
            raise ValueError("无效的网格编码长度")
        
        # 解码网格状态
        grid_state = []
        has_non_empty = False
        for char in encoded_id:
            try:
                value = int(char)
                if value not in [0, 1, 2]:
                    raise ValueError(f"无效的网格状态值: {value}")
                if value != 0:
                    has_non_empty = True
                grid_state.append(value)
            except ValueError:
                raise ValueError(f"无效的网格编码字符: {char}")
        
        # 验证是否有非空白格子
        if not has_non_empty:
            raise ValueError("网格中必须至少有一个非空白格子")
        
        return grid_state, color 