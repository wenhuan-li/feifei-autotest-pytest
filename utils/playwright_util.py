def set_checkbox(page, selector, should_check):
    is_checked = page.is_checked(selector)
    if should_check and not is_checked:
        page.check(selector)
    elif not should_check and is_checked:
        page.uncheck(selector)


def set_multi_select(page, parent, child, options):
    if options is None or len(options) == 0:
        return
    for option in options:
        page.locator(parent).click()
        page.locator(child.replace("#child", option)).first.click()
