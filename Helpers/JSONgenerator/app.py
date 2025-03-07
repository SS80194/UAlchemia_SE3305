import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from encoder import AlchemyRecipeEncoder, RewardGridEncoder
from decoder import AlchemyRecipeDecoder, RewardGridDecoder

# 定义元素属性选项
ELEMENT_PROPERTIES = [
    "火系",
    "水系",
    "草系",
    "雷系"
]

class AlchemyRecipeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("炼金配方JSON生成器")
        
        # 获取屏幕DPI缩放比例
        self.dpi_scale = self.root.winfo_fpixels('1i') / 72
        
        # 根据DPI缩放调整窗口大小
        base_width = 800
        base_height = 600
        scaled_width = int(base_width * self.dpi_scale)
        scaled_height = int(base_height * self.dpi_scale)
        self.root.geometry(f"{scaled_width}x{scaled_height}")
        
        # 创建标签页
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 创建编码器标签页
        self.encoder_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.encoder_frame, text="编码器")
        
        # 创建解码器标签页
        self.decoder_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.decoder_frame, text="解码器")
        
        # 初始化编码器和解码器
        self.recipe_encoder = AlchemyRecipeEncoder()
        self.recipe_decoder = AlchemyRecipeDecoder()
        self.grid_encoder = RewardGridEncoder()
        self.grid_decoder = RewardGridDecoder()
        
        # 初始化材料列表和基本炼金成分列表
        self.materials_list = []
        self.base_elements_list = []
        
        # 设置编码器界面
        self.setup_encoder_ui()
        
        # 设置解码器界面
        self.setup_decoder_ui()
        
        # 配置字体大小
        self.configure_fonts()
    
    def configure_fonts(self):
        # 根据DPI缩放调整字体大小
        base_size = 9
        scaled_size = int(base_size * self.dpi_scale)
        
        # 创建自定义样式
        style = ttk.Style()
        style.configure('.', font=('TkDefaultFont', scaled_size))
        style.configure('Treeview', font=('TkDefaultFont', scaled_size))
        style.configure('TLabel', font=('TkDefaultFont', scaled_size))
        style.configure('TButton', font=('TkDefaultFont', scaled_size))
        style.configure('TEntry', font=('TkDefaultFont', scaled_size))
        
        # 配置Text组件的字体
        text_font = ('TkDefaultFont', scaled_size)
        if hasattr(self, 'json_text'):
            self.json_text.configure(font=text_font)
        if hasattr(self, 'result_text'):
            self.result_text.configure(font=text_font)
    
    def setup_encoder_ui(self):
        # 创建基本信息框架
        basic_frame = ttk.LabelFrame(self.encoder_frame, text="基本信息")
        basic_frame.pack(fill='x', padx=10, pady=5)
        
        # ID输入
        ttk.Label(basic_frame, text="ID:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.id_entry = ttk.Entry(basic_frame)
        self.id_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        
        # 名称输入
        ttk.Label(basic_frame, text="名称:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.name_entry = ttk.Entry(basic_frame)
        self.name_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        
        # 标签输入
        ttk.Label(basic_frame, text="标签 (用逗号分隔):").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.tags_entry = ttk.Entry(basic_frame)
        self.tags_entry.grid(row=2, column=1, sticky='ew', padx=5, pady=5)
        
        # 材料框架
        materials_frame = ttk.LabelFrame(self.encoder_frame, text="材料")
        materials_frame.pack(fill='x', padx=10, pady=5)
        
        # 材料输入区域
        material_input_frame = ttk.Frame(materials_frame)
        material_input_frame.pack(fill='x', padx=5, pady=5)
        
        # 材料类型
        ttk.Label(material_input_frame, text="类型:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.material_type = tk.StringVar(value="class")
        ttk.Radiobutton(material_input_frame, text="类别", variable=self.material_type, value="class").grid(row=0, column=1, sticky='w', padx=5, pady=5)
        ttk.Radiobutton(material_input_frame, text="材料", variable=self.material_type, value="material").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        
        # 材料ID
        ttk.Label(material_input_frame, text="材料ID:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.material_id_entry = ttk.Entry(material_input_frame)
        self.material_id_entry.grid(row=1, column=1, columnspan=2, sticky='ew', padx=5, pady=5)
        
        # 添加材料按钮
        ttk.Button(material_input_frame, text="添加材料", command=self.add_material).grid(row=2, column=0, columnspan=3, pady=5)
        
        # 材料列表显示区域
        self.materials_display = ttk.Frame(materials_frame)
        self.materials_display.pack(fill='x', padx=5, pady=5)
        
        # 基本炼金成分框架
        base_elements_frame = ttk.LabelFrame(self.encoder_frame, text="基本炼金成分")
        base_elements_frame.pack(fill='x', padx=10, pady=5)
        
        # 添加基本炼金成分按钮
        ttk.Button(base_elements_frame, text="添加基本炼金成分", command=self.add_base_element).pack(padx=5, pady=5)
        
        # 基本炼金成分显示区域
        self.base_elements_display = ttk.Frame(base_elements_frame)
        self.base_elements_display.pack(fill='x', padx=5, pady=5)
        
        # 奖励框架
        rewards_frame = ttk.LabelFrame(self.encoder_frame, text="奖励")
        rewards_frame.pack(fill='x', padx=10, pady=5)
        
        # 奖励列表
        self.rewards_list = []
        
        # 添加奖励按钮
        ttk.Button(rewards_frame, text="添加奖励", command=self.add_reward).pack(padx=5, pady=5)
        
        # 奖励显示区域
        self.rewards_display = ttk.Frame(rewards_frame)
        self.rewards_display.pack(fill='x', padx=5, pady=5)
        
        # 操作按钮
        buttons_frame = ttk.Frame(self.encoder_frame)
        buttons_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(buttons_frame, text="生成JSON", command=self.generate_json).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="保存到文件", command=self.save_json).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="清除所有", command=self.clear_encoder).pack(side='left', padx=5)
    
    def add_material(self):
        material_type = self.material_type.get()
        material_id = self.material_id_entry.get().strip()
        
        if not material_id:
            messagebox.showwarning("警告", "请输入材料ID")
            return
        
        material = {
            "type": material_type,
            "id": material_id
        }
        
        self.materials_list.append(material)
        self.update_materials_display()
        
        # 清除输入
        self.material_id_entry.delete(0, 'end')
    
    def update_materials_display(self):
        # 清除现有显示
        for widget in self.materials_display.winfo_children():
            widget.destroy()
        
        # 显示材料列表
        for i, material in enumerate(self.materials_list):
            frame = ttk.Frame(self.materials_display)
            frame.pack(fill='x', pady=2)
            
            ttk.Label(frame, text=f"材料 {i+1}: 类型 {material['type']}, ID: {material['id']}").pack(side='left')
            
            # 删除按钮
            def create_delete_handler(index):
                return lambda: self.delete_material(index)
            
            ttk.Button(frame, text="删除", command=create_delete_handler(i)).pack(side='right')
    
    def delete_material(self, index):
        del self.materials_list[index]
        self.update_materials_display()
    
    def add_base_element(self):
        # 创建基本炼金成分对话框
        element_dialog = tk.Toplevel(self.root)
        element_dialog.title("添加基本炼金成分")
        
        # 根据DPI缩放调整对话框大小
        dialog_width = int(400 * self.dpi_scale)
        dialog_height = int(400 * self.dpi_scale)
        element_dialog.geometry(f"{dialog_width}x{dialog_height}")
        
        element_dialog.transient(self.root)
        element_dialog.grab_set()
        
        # 3x3网格
        ttk.Label(element_dialog, text="3x3网格:").grid(row=0, column=0, columnspan=2, sticky='w', padx=5, pady=5)
        
        grid_frame = ttk.Frame(element_dialog)
        grid_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        # 创建3x3网格
        self.grid_buttons = []
        button_size = int(5 * self.dpi_scale)
        for i in range(3):
            row_buttons = []
            for j in range(3):
                btn = ttk.Button(grid_frame, text=" ", width=button_size)
                btn.grid(row=i, column=j, padx=2, pady=2)
                btn.state = 0
                
                def create_click_handler(button):
                    def on_click():
                        button.state = (button.state + 1) % 3
                        if button.state == 0:
                            button.configure(text=" ")
                        elif button.state == 1:
                            button.configure(text="○")
                        else:
                            button.configure(text="★")
                    return on_click
                
                btn.configure(command=create_click_handler(btn))
                row_buttons.append(btn)
            self.grid_buttons.append(row_buttons)
        
        # 元素属性选择（必选）
        ttk.Label(element_dialog, text="元素:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        element_var = tk.StringVar()
        element_combo = ttk.Combobox(element_dialog, textvariable=element_var, values=ELEMENT_PROPERTIES, state='readonly')
        element_combo.grid(row=2, column=1, sticky='ew', padx=5, pady=5)
        if ELEMENT_PROPERTIES:
            element_combo.set(ELEMENT_PROPERTIES[0])
        
        # 确认按钮
        def confirm_element():
            element = element_var.get()
            
            if not element:
                messagebox.showwarning("警告", "请选择元素")
                return
            
            # 获取网格状态
            grid_state = []
            has_non_empty = False
            for row in self.grid_buttons:
                for btn in row:
                    grid_state.append(btn.state)
                    if btn.state != 0:
                        has_non_empty = True
            
            if not has_non_empty:
                messagebox.showwarning("警告", "网格中必须至少有一个非空白格子")
                return
            
            # 编码网格
            grid_id = self.grid_encoder.encode(grid_state, element)
            
            # 添加到基本炼金成分列表
            element_data = {
                "id": grid_id
            }
            self.base_elements_list.append(element_data)
            
            # 更新显示
            self.update_base_elements_display()
            
            element_dialog.destroy()
        
        ttk.Button(element_dialog, text="确认", command=confirm_element).grid(row=3, column=0, columnspan=2, pady=10)
    
    def update_base_elements_display(self):
        # 清除现有显示
        for widget in self.base_elements_display.winfo_children():
            widget.destroy()
        
        # 显示基本炼金成分列表
        for i, element in enumerate(self.base_elements_list):
            frame = ttk.Frame(self.base_elements_display)
            frame.pack(fill='x', pady=2)
            
            grid_state, color = self.grid_decoder.decode(element['id'])
            display_text = f"成分 {i+1}: "
            if color:
                element_map = {
                    "R": "火系",
                    "B": "水系",
                    "G": "草系",
                    "Y": "雷系"
                }
                element = element_map.get(color, color)
                display_text += f"元素: {element}"
            
            ttk.Label(frame, text=display_text).pack(side='left')
            
            # 删除按钮
            def create_delete_handler(index):
                return lambda: self.delete_base_element(index)
            
            ttk.Button(frame, text="删除", command=create_delete_handler(i)).pack(side='right')
    
    def delete_base_element(self, index):
        del self.base_elements_list[index]
        self.update_base_elements_display()
    
    def add_reward(self):
        # 创建奖励对话框
        reward_dialog = tk.Toplevel(self.root)
        reward_dialog.title("添加奖励")
        
        # 根据DPI缩放调整对话框大小
        dialog_width = int(400 * self.dpi_scale)
        dialog_height = int(500 * self.dpi_scale)
        reward_dialog.geometry(f"{dialog_width}x{dialog_height}")
        
        reward_dialog.transient(self.root)
        reward_dialog.grab_set()
        
        # 奖励等级
        ttk.Label(reward_dialog, text="等级:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        level_entry = ttk.Entry(reward_dialog)
        level_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        
        # 奖励属性（下拉菜单）
        ttk.Label(reward_dialog, text="解锁所需属性:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        property_var = tk.StringVar()
        property_combo = ttk.Combobox(reward_dialog, textvariable=property_var, values=ELEMENT_PROPERTIES, state='readonly')
        property_combo.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        if ELEMENT_PROPERTIES:
            property_combo.set(ELEMENT_PROPERTIES[0])
        
        # 奖励ID (3x3网格)
        ttk.Label(reward_dialog, text="奖励ID (3x3网格):").grid(row=2, column=0, columnspan=2, sticky='w', padx=5, pady=5)
        
        grid_frame = ttk.Frame(reward_dialog)
        grid_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        
        # 创建3x3网格
        self.grid_buttons = []
        button_size = int(5 * self.dpi_scale)  # 调整按钮大小
        for i in range(3):
            row_buttons = []
            for j in range(3):
                btn = ttk.Button(grid_frame, text=" ", width=button_size)
                btn.grid(row=i, column=j, padx=2, pady=2)
                btn.state = 0  # 0: 空白, 1: 圈, 2: 星
                
                # 使用闭包来捕获按钮索引
                def create_click_handler(button):
                    def on_click():
                        button.state = (button.state + 1) % 3
                        if button.state == 0:
                            button.configure(text=" ")
                        elif button.state == 1:
                            button.configure(text="○")
                        else:
                            button.configure(text="★")
                    return on_click
                
                btn.configure(command=create_click_handler(btn))
                row_buttons.append(btn)
            self.grid_buttons.append(row_buttons)
        
        # 网格元素属性选择（必选）
        ttk.Label(reward_dialog, text="非空白格子元素:").grid(row=4, column=0, sticky='w', padx=5, pady=5)
        element_var = tk.StringVar()
        element_combo = ttk.Combobox(reward_dialog, textvariable=element_var, values=ELEMENT_PROPERTIES, state='readonly')
        element_combo.grid(row=4, column=1, sticky='ew', padx=5, pady=5)
        if ELEMENT_PROPERTIES:
            element_combo.set(ELEMENT_PROPERTIES[0])
        
        # 确认按钮
        def confirm_reward():
            try:
                level = int(level_entry.get())
                property_name = property_var.get()
                element = element_var.get()
                
                if not property_name:
                    messagebox.showwarning("警告", "请选择奖励属性")
                    return
                
                if not element:
                    messagebox.showwarning("警告", "请选择元素")
                    return
                
                # 获取网格状态
                grid_state = []
                has_non_empty = False
                for row in self.grid_buttons:
                    for btn in row:
                        grid_state.append(btn.state)
                        if btn.state != 0:
                            has_non_empty = True
                
                if not has_non_empty:
                    messagebox.showwarning("警告", "网格中必须至少有一个非空白格子")
                    return
                
                # 编码网格
                grid_id = self.grid_encoder.encode(grid_state, element)
                
                # 添加到奖励列表
                reward = {
                    "level": level,
                    "property": property_name,
                    "id": grid_id
                }
                self.rewards_list.append(reward)
                
                # 更新显示
                self.update_rewards_display()
                
                reward_dialog.destroy()
            except ValueError:
                messagebox.showerror("错误", "等级必须是数字")
        
        ttk.Button(reward_dialog, text="确认", command=confirm_reward).grid(row=5, column=0, columnspan=2, pady=10)
    
    def update_rewards_display(self):
        # 清除现有显示
        for widget in self.rewards_display.winfo_children():
            widget.destroy()
        
        # 显示奖励列表
        for i, reward in enumerate(self.rewards_list):
            frame = ttk.Frame(self.rewards_display)
            frame.pack(fill='x', pady=2)
            
            ttk.Label(frame, text=f"奖励 {i+1}: 等级 {reward['level']}, 解锁所需属性: {reward['property']}").pack(side='left')
            
            # 删除按钮
            def create_delete_handler(index):
                return lambda: self.delete_reward(index)
            
            ttk.Button(frame, text="删除", command=create_delete_handler(i)).pack(side='right')
    
    def delete_reward(self, index):
        del self.rewards_list[index]
        self.update_rewards_display()
    
    def generate_json(self):
        try:
            # 获取基本信息
            recipe_id = int(self.id_entry.get())
            name = self.name_entry.get()
            # 支持中英文逗号分隔
            tags = [tag.strip() for tag in self.tags_entry.get().replace('，', ',').split(',') if tag.strip()]
            
            # 创建配方数据
            recipe_data = {
                "id": recipe_id,
                "name": name,
                "tags": tags,
                "materials": self.materials_list,
                "base_elements": self.base_elements_list,
                "rewards": self.rewards_list
            }
            
            # 编码为JSON
            json_data = self.recipe_encoder.encode(recipe_data)
            
            # 显示JSON
            json_dialog = tk.Toplevel(self.root)
            json_dialog.title("生成的JSON")
            
            # 根据DPI缩放调整对话框大小
            dialog_width = int(500 * self.dpi_scale)
            dialog_height = int(400 * self.dpi_scale)
            json_dialog.geometry(f"{dialog_width}x{dialog_height}")
            
            text_area = tk.Text(json_dialog, wrap='word', font=('TkDefaultFont', int(9 * self.dpi_scale)))
            text_area.pack(fill='both', expand=True, padx=10, pady=10)
            text_area.insert('1.0', json_data)
            
            # 复制按钮
            def copy_to_clipboard():
                self.root.clipboard_clear()
                self.root.clipboard_append(json_data)
                messagebox.showinfo("成功", "JSON已复制到剪贴板")
            
            ttk.Button(json_dialog, text="复制到剪贴板", command=copy_to_clipboard).pack(pady=10)
            
            return json_data
        except ValueError:
            messagebox.showerror("错误", "ID必须是数字")
            return None
    
    def save_json(self):
        json_data = self.generate_json()
        if json_data:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
            )
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(json_data)
                messagebox.showinfo("成功", f"JSON已保存到 {file_path}")
    
    def clear_encoder(self):
        # 清除所有输入
        self.id_entry.delete(0, 'end')
        self.name_entry.delete(0, 'end')
        self.tags_entry.delete(0, 'end')
        self.material_type.set("class")
        self.material_id_entry.delete(0, 'end')
        self.materials_list = []
        self.base_elements_list = []
        self.rewards_list = []
        self.update_materials_display()
        self.update_base_elements_display()
        self.update_rewards_display()
    
    def setup_decoder_ui(self):
        # 解码器控制框架
        control_frame = ttk.Frame(self.decoder_frame)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(control_frame, text="加载JSON文件", command=self.load_json_file).pack(side='left', padx=5)
        ttk.Button(control_frame, text="解析JSON", command=self.parse_json).pack(side='left', padx=5)
        
        # JSON输入区域
        json_frame = ttk.LabelFrame(self.decoder_frame, text="JSON输入")
        json_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.json_text = tk.Text(json_frame, wrap='word', height=10, font=('TkDefaultFont', int(9 * self.dpi_scale)))
        self.json_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # 解析结果区域
        result_frame = ttk.LabelFrame(self.decoder_frame, text="解析结果")
        result_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.result_text = tk.Text(result_frame, wrap='word', height=10, state='disabled', font=('TkDefaultFont', int(9 * self.dpi_scale)))
        self.result_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    def load_json_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    json_content = f.read()
                self.json_text.delete('1.0', 'end')
                self.json_text.insert('1.0', json_content)
            except Exception as e:
                messagebox.showerror("错误", f"无法加载文件: {str(e)}")
    
    def parse_json(self):
        try:
            json_content = self.json_text.get('1.0', 'end').strip()
            if not json_content:
                messagebox.showwarning("警告", "请先输入JSON内容")
                return
            
            # 解析JSON
            recipe_data = self.recipe_decoder.decode(json_content)
            
            # 显示解析结果
            self.result_text.config(state='normal')
            self.result_text.delete('1.0', 'end')
            
            # 格式化显示
            result = f"ID: {recipe_data['id']}\n"
            result += f"名称: {recipe_data['name']}\n"
            result += f"标签: {', '.join(recipe_data['tags'])}\n\n"
            
            result += "材料:\n"
            for i, material in enumerate(recipe_data['materials']):
                result += f"  材料 {i+1}: 类型 {material['type']}, ID: {material['id']}\n"
            result += "\n"
            
            result += "基本炼金成分:\n"
            for i, element in enumerate(recipe_data.get('base_elements', [])):
                result += f"  成分 {i+1}:\n"
                grid_state, color = self.grid_decoder.decode(element['id'])
                grid_text = "    网格:\n"
                
                for row in range(3):
                    grid_text += "      "
                    for col in range(3):
                        idx = row * 3 + col
                        if grid_state[idx] == 0:
                            grid_text += "□ "
                        elif grid_state[idx] == 1:
                            grid_text += "○ "
                        else:
                            grid_text += "★ "
                    grid_text += "\n"
                
                if color:
                    element_map = {
                        "R": "火系",
                        "B": "水系",
                        "G": "草系",
                        "Y": "雷系"
                    }
                    element = element_map.get(color, color)
                    grid_text += f"    元素: {element}\n"
                
                result += grid_text + "\n"
            
            result += "奖励:\n"
            for i, reward in enumerate(recipe_data['rewards']):
                result += f"  奖励 {i+1}:\n"
                result += f"    等级: {reward['level']}\n"
                result += f"    解锁所需属性: {reward['property']}\n"
                
                # 解码网格
                grid_state, color = self.grid_decoder.decode(reward['id'])
                grid_text = "    网格:\n"
                
                for row in range(3):
                    grid_text += "      "
                    for col in range(3):
                        idx = row * 3 + col
                        if grid_state[idx] == 0:
                            grid_text += "□ "
                        elif grid_state[idx] == 1:
                            grid_text += "○ "
                        else:
                            grid_text += "★ "
                    grid_text += "\n"
                
                if color:
                    element_map = {
                        "R": "火系",
                        "B": "水系",
                        "G": "草系",
                        "Y": "雷系"
                    }
                    element = element_map.get(color, color)
                    grid_text += f"    非空白格子元素: {element}\n"
                
                result += grid_text + "\n"
            
            self.result_text.insert('1.0', result)
            self.result_text.config(state='disabled')
            
        except Exception as e:
            messagebox.showerror("错误", f"解析JSON失败: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AlchemyRecipeApp(root)
    root.mainloop() 