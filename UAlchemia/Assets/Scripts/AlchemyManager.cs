using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AlchemyManager : MonoBehaviour
{
    // 定义页面枚举
    public enum PanelType
    {
        SelectionPanel,
        MaterialsPanel,
        PuzzlePanel,
        SuccessPanel
    }
    
    // 页面引用
    public GameObject SelectionPanel;
    public GameObject MaterialsPanel;
    public GameObject PuzzlePanel;
    public GameObject SuccessPanel;
    
    // 页面历史栈
    private Stack<PanelType> panelHistory = new Stack<PanelType>();
    private PanelType currentPanel;
    
    // Start is called before the first frame update
    void Start()
    {
        // 初始化为SelectionPanel
        HideAllPanels();
        ShowPanel(PanelType.SelectionPanel);
        currentPanel = PanelType.SelectionPanel;
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    
    // 隐藏所有面板
    private void HideAllPanels()
    {
        SelectionPanel.SetActive(false);
        MaterialsPanel.SetActive(false);
        PuzzlePanel.SetActive(false);
        SuccessPanel.SetActive(false);
    }
    
    // 显示指定面板
    private void ShowPanel(PanelType panelType)
    {
        HideAllPanels();
        
        switch (panelType)
        {
            case PanelType.SelectionPanel:
                SelectionPanel.SetActive(true);
                break;
            case PanelType.MaterialsPanel:
                MaterialsPanel.SetActive(true);
                break;
            case PanelType.PuzzlePanel:
                PuzzlePanel.SetActive(true);
                break;
            case PanelType.SuccessPanel:
                SuccessPanel.SetActive(true);
                break;
        }
    }
    
    // 跳转到材料面板
    public void GotoMaterialsPanel()
    {
        panelHistory.Push(currentPanel);
        currentPanel = PanelType.MaterialsPanel;
        ShowPanel(currentPanel);
    }
    
    // 跳转到拼图面板
    public void GotoPuzzlePanel()
    {
        panelHistory.Push(currentPanel);
        currentPanel = PanelType.PuzzlePanel;
        ShowPanel(currentPanel);
    }
    
    // 跳转到成功面板
    public void GotoSuccessPanel()
    {
        panelHistory.Push(currentPanel);
        currentPanel = PanelType.SuccessPanel;
        ShowPanel(currentPanel);
    }
    
    // 跳转到选择面板
    public void GotoSelectionPanel()
    {
        panelHistory.Push(currentPanel);
        currentPanel = PanelType.SelectionPanel;
        ShowPanel(currentPanel);
    }

    public bool GoBack()
    {
        // 如果历史栈中有页面，则返回上一个页面
        if (panelHistory.Count > 0)
        {
            currentPanel = panelHistory.Pop();
            ShowPanel(currentPanel);
            return true;
        }
        
        // 无法返回
        return false;
    }
}
