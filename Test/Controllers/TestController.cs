public TestController : Controller
{
	public ActionView UsedView()
	{
		return View();
	}

	public ActionView GetSameViewAsAbove()
	{
		return View("UsedView");
	}
}