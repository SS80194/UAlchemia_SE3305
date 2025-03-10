using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class PageManager : MonoBehaviour
{
    // 页面引用
    public GameObject mainPage;     // 主页面(取代了homePage)
    public GameObject alchemyPage;
    public GameObject comissionPage;
    public GameObject savePage;     // 重新加回保存页面
    public GameObject shopPage;     // 新增商店页面
    
    // 返回按钮引用集合
    public Button[] backButtons;    // 改为按钮数组，收集所有页面的返回按钮
    
    // 当前页面和上一个页面的引用
    private GameObject currentPage;
    private GameObject previousPage;
    
    // 页面历史栈
    private Stack<GameObject> pageHistory = new Stack<GameObject>();

    // Start is called before the first frame update
    void Start()
    {
        // 初始显示主页
        currentPage = mainPage;
        ShowPage(mainPage);
        HideOtherPages(mainPage);
        
        // 将主页压入栈
        pageHistory.Push(mainPage);
        
        // 为所有返回按钮添加监听
        if (backButtons != null && backButtons.Length > 0)
        {
            foreach (Button button in backButtons)
            {
                if (button != null)
                {
                    button.onClick.AddListener(GoBack);
                }
            }
        }
        else
        {
            Debug.LogWarning("未设置返回按钮，请在Inspector中设置PageManager的backButtons数组");
        }
    }

    // Update is called once per frame
    void Update()
    {
        // 检测右键点击返回
        if (Input.GetMouseButtonDown(1) && pageHistory.Count > 1)
        {
            GoBack();
        }
    }
    
    // 显示指定页面
    private void ShowPage(GameObject page)
    {
        if (page != null)
        {
            page.SetActive(true);
        }
    }
    
    // 隐藏指定页面
    private void HidePage(GameObject page)
    {
        if (page != null)
        {
            page.SetActive(false);
        }
    }
    
    // 隐藏除了指定页面外的所有页面
    private void HideOtherPages(GameObject currentPage)
    {
        GameObject[] allPages = { mainPage, alchemyPage, comissionPage, savePage, shopPage };
        
        foreach (GameObject page in allPages)
        {
            if (page != null && page != currentPage)
            {
                page.SetActive(false);
            }
        }
    }
    
    // 通用页面跳转方法
    private void NavigateToPage(GameObject targetPage)
    {
        if (targetPage != currentPage)
        {
            previousPage = currentPage;
            currentPage = targetPage;
            
            // 将新页面压入历史栈
            pageHistory.Push(targetPage);
            
            ShowPage(targetPage);
            HideOtherPages(targetPage);
        }
    }
    
    // 跳转到主页
    public void GoToMainPage()
    {
        // 清空历史栈并重新设置主页
        pageHistory.Clear();
        currentPage = mainPage;
        pageHistory.Push(mainPage);
        ShowPage(mainPage);
        HideOtherPages(mainPage);
    }
    
    // 跳转到炼金页面
    public void GoToAlchemyPage()
    {
        NavigateToPage(alchemyPage);
    }
    
    // 跳转到委托页面
    public void GoToComissionPage()
    {
        NavigateToPage(comissionPage);
    }
    
    // 跳转到保存页面
    public void GoToSavePage()
    {
        NavigateToPage(savePage);
    }
    
    // 跳转到商店页面
    public void GoToShopPage()
    {
        NavigateToPage(shopPage);
    }
    
    // 返回上一个页面
    public void GoBack()
    {
        // 如果栈中至少有两个页面（当前页面和上一个页面）
        if (pageHistory.Count > 1)
        {
            // 弹出当前页面
            pageHistory.Pop();
            
            // 获取上一个页面
            GameObject previousPage = pageHistory.Peek();
            
            // 切换到上一个页面
            currentPage = previousPage;
            ShowPage(currentPage);
            HideOtherPages(currentPage);
        }
        else if (currentPage != mainPage)
        {
            // 如果栈中只有一个页面且不是主页，返回主页
            pageHistory.Clear();
            pageHistory.Push(mainPage);
            currentPage = mainPage;
            ShowPage(mainPage);
            HideOtherPages(mainPage);
        }
    }
}
