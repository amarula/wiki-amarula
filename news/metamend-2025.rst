==============================================================================
Amarula Launches meta-mend: Enhancing Yocto Security with Mend SCA Integration
==============================================================================

**Treviso, Italy - May 17, 2025** - Amarula, a company specializing in security solutions and dedicated to assisting organizations with compliance, including the upcoming Cyber Resilience Act (CRA) in Europe, today announced the release of ``meta-mend``, a new layer for the Yocto Project. This innovative layer provides seamless integration of Mend Software Composition Analysis (SCA) directly into the Yocto build process, empowering developers to proactively identify and mitigate open-source vulnerabilities within their embedded Linux distributions.

``meta-mend`` introduces a dedicated BitBake class that simplifies the application of Mend's powerful SCA capabilities. By leveraging Mend's extensive vulnerability database and analysis tools, Yocto developers can gain critical insights into the security risks associated with the open-source components included in their embedded systems. This allows for timely remediation and the development of more secure and resilient products.

The layer is designed for ease of use and requires minimal configuration. Users can enable Mend checks by simply inheriting the ``mend`` class in their Yocto configuration and providing their Mend API credentials. To streamline the setup of the necessary Java runtime environment for Mend analysis, Amarula provides a custom ``kas-container`` image that includes Java. This container image is readily available for download.

"In today's rapidly evolving threat landscape and with the impending Cyber Resilience Act in Europe, ensuring the security of embedded systems is paramount," said a representative from Amarula. "``meta-mend`` is a direct response to this need, providing a straightforward way for Yocto developers to integrate industry-leading SCA into their workflow. Our expertise in security and regulatory compliance allows us to develop solutions that truly address the challenges our customers face."

**Key benefits of ``meta-mend``:**

* **Seamless Mend SCA Integration:** Directly incorporate Mend's vulnerability analysis into the Yocto build process.
* **Early Vulnerability Detection:** Identify and address open-source risks early in the development lifecycle.
* **Enhanced Security Posture:** Build more secure and resilient embedded Linux distributions.
* **Simplified Setup:** Easy configuration with a dedicated BitBake class.
* **Optional ``kas-container`` with Java:** Provides a ready-to-use environment for Mend analysis.
* **Alignment with CRA:** Helps organizations meet emerging cybersecurity regulations in Europe.

**Availability:**

The ``meta-mend`` layer is available for download at https://github.com/amarula/meta-mend. Amarula encourages developers to explore the layer and contribute to its ongoing development.

**About Amarula:**

Amarula is a company specializing in security solutions for embedded systems. With a deep understanding of security best practices and emerging regulations like the Cyber Resilience Act in Europe, Amarula is committed to providing tools and expertise that help organizations build secure and compliant products.

**Contact:**

[https://www.amarulasolutions.com/contact/]
