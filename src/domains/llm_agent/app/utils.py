from Markdown2docx import Markdown2docx
from io import BytesIO
import tempfile
import os
import logging

def convert_md_to_docx(md_content: str) -> BytesIO:
    md_path = None
    docx_path = None
    try:
        # Создаем временный markdown файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as md_file:
            md_file.write(md_content)
            md_path = md_file.name

        # Определяем путь docx-файла, который сгенерирует Markdown2docx
        docx_path = md_path.replace('.md', '.docx')  # Важно!

        # Инициализируем и конвертируем
        project = Markdown2docx(md_path[:-3])  # Инициализируем без расширения md!
        project.eat_soup()  # Обрабатываем markdown
        project.save()      # Сохраняем как docx

        # Проверяем: действительно ли docx-файл существует и не пустой
        if not os.path.isfile(docx_path) or os.path.getsize(docx_path) == 0:
            raise ValueError("Generated DOCX file is empty")

        # Читаем docx-файл в память
        with open(docx_path, 'rb') as f:
            docx_bytes = f.read()
        docx_buffer = BytesIO(docx_bytes)
        docx_buffer.seek(0)

        return docx_buffer

    except Exception as e:
        logging.error(f"DOCX conversion error: {e}")
        raise
    finally:
        # Удаляем временные файлы
        if md_path and os.path.exists(md_path):
            os.unlink(md_path)
        if docx_path and os.path.exists(docx_path):
            os.unlink(docx_path)

if __name__ == "__main__":
    res = convert_md_to_docx('''
    # Russia-Azerbaijan Relations: A Comprehensive Analysis of Cooperation, Divergence, and Regional Implications

## Introduction

The relationship between Russia and Azerbaijan is a critical, yet complex, dynamic shaping the geopolitical landscape of the South Caucasus. Marked by a pragmatic blend of economic cooperation, strategic alignment, and underlying tensions, this partnership significantly impacts regional stability, energy security, and conflict mitigation efforts. This report provides a comprehensive analysis of Russia-Azerbaijan relations, moving beyond superficial observations to explore the historical context, current state of cooperation, and potential future challenges. Understanding the nuances of this relationship is increasingly vital given the ongoing volatility in the region and the broader implications for European energy markets.

This investigation builds upon the foundation of shared interests – particularly in the energy sector – while critically examining emerging divergences in approaches to regional security. The analysis reveals how seemingly minor diplomatic and economic initiatives have historically shaped the power balance, laying the groundwork for both cooperation and potential conflict, as evidenced by the shifting dynamics surrounding the Nagorno-Karabakh conflict. Furthermore, this report addresses the critical role Azerbaijan plays as a transit country for Russian energy, and how this interdependence contributes to, but does not guarantee, regional stability.

The objective of this report is to provide a nuanced understanding of the factors driving Russia-Azerbaijan relations, identify potential flashpoints, and assess the long-term implications for regional security and energy markets. Through a detailed examination of historical context, current cooperation initiatives, and projected future challenges, this analysis aims to inform policymakers and stakeholders invested in the stability of the South Caucasus. The analysis draws upon available documentation, including historical records, geopolitical analyses, and limited interview data, to provide a comprehensive assessment of this crucial partnership. 

This report is structured as follows: Section 2 examines the historical and political context underpinning Russia-Azerbaijan relations. Section 3 details the current state of cooperation, with a focus on energy security initiatives. Finally, Section 4 explores the prospects and challenges facing this relationship, with specific attention paid to diverging approaches to conflict mitigation and the implications for regional stability. Through this structure, this report provides a cohesive and insightful analysis of this strategically important partnership.





## 1. Историко-политический контекст отношений

### Insights

The relationship between Russia and Azerbaijan, particularly concerning the Nagorno-Karabakh conflict, is characterized by a complex interplay of interests often masked by outwardly amicable diplomatic initiatives. A compelling example of this dynamic occurred in the mid-1990s, following the First Nagorno-Karabakh War. Between 1995 and 1997, Russia engaged in a series of bilateral agreements with Azerbaijan focused on energy cooperation, granting Russian companies preferential access to Azerbaijani oil and gas resources in exchange for Moscow’s support of Baku’s economic development [1].

While seemingly standard economic agreements, their timing and implications were far-reaching. Azerbaijan, economically devastated by the war, sought to rebuild its infrastructure and attract foreign investment. Russia, despite post-Soviet economic challenges, possessed the technical expertise and financial resources Azerbaijan needed [1]. Critically, this arrangement subtly facilitated a build-up of Azerbaijani military capabilities, with Russia providing weapons systems through opaque arms deals that allowed Baku to gradually reverse the military balance lost in the first war [1]. 

This strategy stemmed from several key factors. Firstly, Russia recognized that a perpetually frozen conflict in Nagorno-Karabakh maintained its influence over both Armenia and Azerbaijan, as a fully resolved conflict would diminish its regional leverage. Secondly, Russia prioritized Azerbaijan as a vital energy partner, seeking long-term cooperation. Finally, the economic agreements fostered a degree of dependency between Baku and Moscow, discouraging Azerbaijan from antagonizing Russia [1]. 

This subtle shift in the balance of power, facilitated by these seemingly minor diplomatic and economic initiatives, ultimately laid the groundwork for the Second Nagorno-Karabakh War in 2020. Azerbaijan’s decisive victory, enabled by years of Russian support and a significantly strengthened military, fundamentally altered the regional landscape. This demonstrates how diplomatic initiatives, even those presented as purely economic or peacekeeping in nature, can have profound and unforeseen consequences in conflict zones [1]. This case highlights the importance of analyzing not just the stated objectives of diplomatic initiatives, but also the underlying strategic calculations and potential long-term impacts.

### Sources

[1] Elena Volkov, Senior Historian & Geopolitical Analyst, Institute for Strategic Studies – Black Sea Region.

---

## 2. Современное состояние российско-азербайджанского сотрудничества

### Insights

The relationship between Russia and Azerbaijan plays a crucial role in regional energy security, extending beyond established pipeline projects. While specific instances of disruption mitigation *beyond* existing infrastructure are not detailed within the provided documentation, the broader context of the Iran-Iraq War [2] illuminates the stabilizing effect of their cooperation. The conflict demonstrated how vulnerable supply routes can be, and by extension, how vital secure transit corridors are to regional stability. Azerbaijan functions as a key transit country for Russian energy reaching Turkey and Europe; maintaining this cooperation is inherently a mitigation strategy against potential supply disruptions. 

The historical context of the Iran-Iraq War [2] demonstrates the importance of secure supply lines, mirroring the current dynamic in the Russia-Azerbaijan relationship. Cooperation also extends to the exploration and potential development of Caspian Sea energy resources, reducing reliance on external sources and enhancing energy security for both nations. This collaborative effort, while complex financially and logistically, is facilitated by the existing cooperative frameworks. 

However, the Iran-Iraq War [2] also serves as a cautionary tale, implicitly demonstrating the risks posed by regional conflict and geopolitical tensions. These factors could potentially disrupt the current cooperative dynamic between Russia and Azerbaijan. The absence of detailed specifics regarding mitigation *beyond* established pipelines underscores the need for further investigation into collaborative projects focused on diversifying routes and increasing capacity. In essence, Russian-Azerbaijani energy cooperation contributes to regional stability by providing diversified supply routes and fostering joint resource development.

### Sources

[1] Elena Volkov, Senior Historian & Geopolitical Analyst, Institute for Strategic Studies – Black Sea Region.
[2] en.wikipedia.org, page 7.

---

## 3. Перспективы и вызовы двусторонних отношений

### Insights

The relationship between Russia and Azerbaijan, while characterized by a shared stated interest in regional stability, demonstrates nuanced divergences in approach to conflict mitigation which could impact long-term security cooperation. Given the increasing volatility in the South Caucasus, understanding these divergences is critical. 

While both Russia and Azerbaijan benefit from a degree of stability in the region, their definitions and methods for achieving it appear to differ.  Azerbaijan likely prioritizes the consolidation of its territorial integrity and sovereign control, potentially through assertive actions, while Russia’s approach appears more focused on maintaining its regional influence and leveraging its role as a security guarantor. This difference manifests in approaches to conflict mitigation. 

Specifically, while there is currently limited detailed public information available, the broad dynamic points to a potential disconnect between Azerbaijan’s desire for unilateral security measures and Russia’s preference for multilateral frameworks, potentially hindering coordinated border security efforts. Furthermore, differing perspectives on regional actors and the interpretation of “stability” could complicate non-proliferation initiatives, particularly regarding the flow of arms and technologies [3]. 

The long-term prospects for cooperation hinge on addressing these divergences through consistent dialogue and the establishment of clear, mutually agreed-upon security protocols. Failure to do so could lead to increased mistrust, fragmented security architectures, and ultimately, a heightened risk of instability. Further research is needed to identify specific instances of diverging approaches and to assess the practical implications for border security and non-proliferation efforts.

### Sources

[1] Elena Volkov, Senior Historian & Geopolitical Analyst, Institute for Strategic Studies – Black Sea Region.
[2] en.wikipedia.org, page 7.
[3] Limited sources available at this time. Analysis relies on interview data and publicly available information. Further research required for a more comprehensive assessment.
---


## Conclusion

The analysis of Russia-Azerbaijan relations reveals a complex partnership fundamentally shaped by a pragmatic convergence of interests – energy security, regional stability, and a mutual desire to navigate the volatile South Caucasus. This report demonstrates that the relationship, while outwardly cooperative, is built upon a foundation of nuanced strategic calculations and, increasingly, diverging approaches to achieving those shared goals. The initial period of cooperation, highlighted by energy agreements following the First Nagorno-Karabakh War, was not merely economic. It constituted a calculated Russian strategy to bolster Azerbaijan’s military capabilities, subtly reshaping the regional balance of power and ultimately laying the groundwork for the 2020 conflict.

This pragmatic underpinning continues to define the relationship today. The enduring energy partnership, as evidenced by the reliance on Azerbaijani transit routes, serves as a crucial stabilizing factor for both nations and a vital component of broader European energy security. However, the report also reveals an evolving dynamic. While Russia and Azerbaijan share a stated interest in regional stability, their definitions and preferred methods for achieving it demonstrate increasing divergence. Azerbaijan’s focus on consolidating territorial integrity and asserting sovereign control, potentially through unilateral action, appears to contrast with Russia’s preference for maintaining its regional influence through a more multilateral, guarantor-based approach. This divergence, though currently subtle, risks hindering coordinated efforts on critical issues like border security and non-proliferation.

The implications of this evolving dynamic are significant. Continued cooperation requires consistent, transparent dialogue to address these diverging priorities and establish clear, mutually agreed-upon security protocols. Failure to do so could lead to increased mistrust, fragmented regional security architectures, and ultimately, a heightened risk of instability in an already volatile region. The lack of readily available, detailed documentation throughout this analysis underscores the need for further, in-depth research into the specific instances of diverging approaches and their practical consequences. 

This report highlights that the Russia-Azerbaijan relationship is not static. It is a dynamic partnership shaped by historical context, geopolitical realities, and evolving national interests. Understanding this complexity is crucial not only for policymakers and analysts but also for anyone seeking to navigate the intricacies of the South Caucasus. Future research should prioritize a deeper examination of the evolving security landscape, focusing on specific instances of cooperation and divergence, and assessing the long-term implications for regional stability and energy security. Ultimately, sustained analytical attention and open dialogue are essential to ensure that this pragmatic partnership continues to contribute to a more secure and prosperous future for the region.





## Sources

[1] Elena Volkov, Senior Historian & Geopolitical Analyst, Institute for Strategic Studies – Black Sea Region.
[2] en.wikipedia.org, page 7.
[3] Limited sources available at this time. Analysis relies on interview data and publicly available information. Further research required for a more comprehensive assessment.

    ''')