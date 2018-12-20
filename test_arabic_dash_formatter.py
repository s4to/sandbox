# coding: utf-8

from arabic_dash_formatter import formatting_page_no


def main():

    # Test
    import filecmp
    resources_dir = "test/resources/"
    results_dir = "test/results/"
    true_dir = "test/true/"

    # pdf to docx
    pdf_to_docx_footer = "footer1.xml"
    footer = formatting_page_no(resources_dir + pdf_to_docx_footer)
    with open(results_dir + pdf_to_docx_footer, 'w') as _f:
        _f.write(str(footer))

    assert(filecmp.cmp(results_dir + pdf_to_docx_footer, true_dir + pdf_to_docx_footer))

    # PAGEの両端にダッシュを含む
    dash_footer = "footer2.xml"
    footer = formatting_page_no(resources_dir + dash_footer)
    with open(results_dir + dash_footer, 'w') as _f:
        _f.write(str(footer))

    assert(filecmp.cmp(results_dir + dash_footer, true_dir + dash_footer))


if __name__ == '__main__':
    main()

