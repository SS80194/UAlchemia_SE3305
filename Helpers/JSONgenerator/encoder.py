import json

class AlchemyRecipeEncoder:
    """炼金配方编码器，将配方数据转换为JSON格式"""
    
    def encode(self, recipe_data):
        """
        将配方数据编码为JSON字符串
        
        参数:
            recipe_data: 包含配方信息的字典
        
        返回:
            JSON格式的字符串
        """
        # 验证必要的字段
        required_fields = ['id', 'name', 'tags', 'materials', 'base_elements', 'rewards']
        for field in required_fields:
            if field not in recipe_data:
                raise ValueError(f"缺少必要的字段: {field}")
        
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
        
        # 验证奖励字段
        for i, reward in enumerate(recipe_data['rewards']):
            if 'level' not in reward or 'property' not in reward or 'id' not in reward:
                raise ValueError(f"奖励 {i+1} 缺少必要的字段")
        
        # 转换为JSON
        return json.dumps(recipe_data, ensure_ascii=False, indent=2)


class RewardGridEncoder:
    """奖励网格编码器，将3x3网格状态编码为ID字符串"""
    
    def encode(self, grid_state, color):
        """
        将3x3网格状态编码为ID字符串
        
        参数:
            grid_state: 长度为9的列表，表示3x3网格的状态 (0:空白, 1:圈, 2:星)
            color: 非空白格子（圈和星）的颜色
        
        返回:
            编码后的ID字符串
        """
        if len(grid_state) != 9:
            raise ValueError("网格状态必须是长度为9的列表")
        
        # 验证网格状态值
        has_non_empty = False
        for value in grid_state:
            if value not in [0, 1, 2]:
                raise ValueError("网格状态值必须是 0, 1 或 2")
            if value != 0:
                has_non_empty = True
        
        if not has_non_empty:
            raise ValueError("网格中必须至少有一个非空白格子")
        
        if not color:
            raise ValueError("必须指定非空白格子的元素属性")
        
        # 编码网格状态
        encoded_id = ""
        
        # 添加网格状态
        for value in grid_state:
            encoded_id += str(value)
        
        # 添加颜色信息
        color_map = {
            "火系": "R",
            "水系": "B",
            "草系": "G",
            "雷系": "Y"
        }
        if color not in color_map:
            raise ValueError("无效的元素属性")
        
        encoded_id += ":" + color_map[color]
        
        return encoded_id 