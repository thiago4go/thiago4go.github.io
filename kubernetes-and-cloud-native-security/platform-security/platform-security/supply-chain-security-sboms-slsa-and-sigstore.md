---
description: By Thiago S Shimada Ramos
---

# Supply Chain Security: SBOMs, SLSA, and Sigstore

In today's complex software world, every piece of code we use can be a potential entry point for vulnerabilities. As our systems become more intricate, it's essential to have strong safeguards and proven methods to ensure the software we rely on is secure and trustworthy. Without these fundamental security measures and a clear strategy for growth, it's almost impossible to predict or handle future security threats effectively.

Through ongoing research and collaboration with the security community, it's clear that robust cloud-native security is more than just individual tools or settings. It's about strategically layering multiple security solutions to create a truly protected environment. Let's explore these essential security layers together.

Imagine the need to balance adaptability with strict control. Achieving this balance in security can be challenging, but with the right tools and strategies – such as SBOMs, SLSA, and Sigstore – securing your Kubernetes supply chain becomes a manageable process.

<figure><img src="../../.gitbook/assets/SBOM (1).png" alt=""><figcaption><p>Supply Chain Security</p></figcaption></figure>

## **Initial Security Challenges in Kubernetes**

**Growing Complexity:** The rise of advanced technologies like GenAI and microservices has led to more complex systems with numerous interconnected parts. This complexity has revealed potential weaknesses in container images, with many teams finding numerous vulnerabilities hidden within.

**Third-Party Risks:** Over 60% of organizations using Kubernetes have reported security incidents linked to compromised or outdated software components from external sources.

**Protecting Sensitive Data:** With GenAI handling valuable data, attackers are motivated to not only steal data but also to potentially corrupt or manipulate AI models, highlighting the need for robust security throughout the software supply chain.

## Key Components of Modern Supply-Chain Security

* **SBOM (Software Bill of Materials):** SBOMs have evolved from simple lists of software components to advanced standards like [SPDX ](https://slsa.dev/blog/2022/05/slsa-sbomSPDXSPDX)and [CycloneDX](https://github.com/CycloneDX/specification). Tools like [Trivy ](https://github.com/aquasecurity/trivy)and [Syft ](https://github.com/anchore/syft)can be easily integrated into software development pipelines to automatically create SBOMs. Major tech companies are also contributing to the SBOM ecosystem; for example, [Microsoft](https://github.com/microsoft/sbom-tool) has open-sourced its `sbom-tool`, which helps generate SPDX-compatible SBOMs for various operating systems. Think of an SBOM as an ingredient list for your software, detailing everything that goes into it.
  * **Visibility and Transparency:** An SBOM gives you a clear view of all the components in your software, including libraries and their dependencies, enhancing transparency and understanding of your software's composition.
  * **Proactive Vulnerability Management:** SBOMs enable continuous monitoring for vulnerabilities. By comparing your SBOMs against regularly updated vulnerability databases, you can quickly identify and address new threats in your existing software.
  * **Kubernetes Integration:** Kubernetes can be configured to use SBOMs to automatically block software images that lack an SBOM or contain critical security flaws, adding an automated layer of defense. Platforms like [GitLab ](https://about.gitlab.com/solutions/supply-chain/)can streamline this process by integrating SBOM generation and vulnerability scanning directly into their CI/CD pipelines.
* **SLSA (Supply-chain Levels for Software Artifacts):** [SLSA ](https://slsa.dev)(pronounced as Salsa) is a step-by-step framework for improving software integrity. It ranges from basic tracking of software origins (Level 1) to highly secure, tamper-proof builds with verified origins (Level 4). SLSA provides a structured way to build confidence in your software's security.
  * **Verifiable Build Origins:** SLSA's primary goal is to ensure you can trace exactly how, when, and where a software component was built, providing essential provenance information.
  * **Four Levels of Security Assurance:** SLSA offers increasing levels of security:
    * **Level 1:** Basic origin tracking.
    * **Level 2:** Tamper-evident builds with signed metadata.
    * **Level 3:** Isolated and consistent build environments.
    * **Level 4:** Fully verifiable and unchangeable build processes.
  * **Proven Effectiveness:** Real-world examples, like [Google Cloud'](https://cloud.google.com/blog/products/identity-security/how-were-making-gke-more-secure-with-supply-chain-attestation-and-slsa)s adoption of SLSA show its commitment to providing you with the tools and capabilities needed to help build and manage secure, transparent software supply chains.
* **Sigstore:** [Sigstore ](https://www.sigstore.dev/)offers a suite of user-friendly cryptographic tools, including [Cosign](https://github.com/sigstore/cosign), [Fulcio](https://github.com/sigstore/fulcio), and [Rekor](https://github.com/sigstore/rekor), designed to simplify the process of signing and verifying software. This ensures that containers and software packages are validated before being used in Kubernetes.
  * **Cosign:** Sigstore’s Cosign tool simplifies the process of digitally signing container images and Kubernetes configurations without the complexities of traditional key management systems.
  * **Fulcio & Rekor:** Fulcio provides short-term security certificates, while Rekor maintains a permanent, unalterable record of these certifications. Together, they prevent tampering and replay attacks, ensuring the integrity of your software.
  * **Automated Policy Enforcement:** Sigstore’s Policy Controller can be integrated into Kubernetes to automatically reject software containers that are not properly signed or lack valid certifications, enforcing security policies automatically.

## **Completing the Security Framework: Continuous Monitoring and Policy**

* **Vulnerability Scanning:** Tools like Aqua Security and Trivy analyze software images using SBOM data to identify vulnerabilities and prevent the deployment of software that doesn't meet your security standards.
* **Policy as Code:** Using tools like OPA (Open Policy Agent), you can define your security rules—such as SLSA compliance or mandatory Sigstore signatures—in a centralized, code-based policy system for consistent enforcement.
* **Real-time Monitoring:** Solutions like Falco, Uptycs, and Calico monitor your running containers and systems in real-time to detect and alert on unusual behavior, providing an active defense against threats.

## **Practical Steps and Use Cases**

Here’s a step-by-step plan to strengthen your Kubernetes supply chain security:

### **Phase 1: Essential Security Foundations**

* **Automate SBOM Creation:**
  * **How:** Integrate SBOM tools like Syft or Trivy into your software build process (CI/CD pipeline).
  * Attach SBOMs to container images using Cosign.
* **Implement Basic Security Policies:**
  * **How:** Deploy Sigstore Policy Controller to enforce at least minimal SBOM checks for mission-critical namespaces.
* **Achieve SLSA Level 1 Security:**
  * **How:** Ensure your software builds are authenticated, software dependencies are clearly defined, and document the basic steps of your build process.

### **Phase 2: Enhanced Security Measures**

* **Implement Keyless Signing with Sigstore:**
  * **How:** Set up Fulcio and Rekor for managing short-term certificates and use Cosign to sign your software.
* **Reach SLSA Level 3 Security:**
  * **How:** Utilize tools like Tekton Chains or GitHub Actions to create isolated, repeatable software builds.
  * Generate detailed records (attestations) for each step in the build process.
* **Real-time Security Verification and Monitoring:**
  * **How:** Deploy Falco or Uptycs to continuously monitor for unusual activities and connect SBOM data with running processes for enhanced threat detection.

### **Phase 3: Ongoing Security Assurance**

* **Define Security Policy as Code:**
  * **How:** Create OPA/Rego policies to enforce key security requirements, such as mandatory Sigstore signatures and blocking software with critical vulnerabilities.
* **Establish Attestation Chains:**
  * **How:** Require that SLSA build process records (metadata) are in place before software is signed with Sigstore, creating a complete chain of trust from the initial code commit to the running software.
* **Regular Security Testing:**
  * **How:** Use tools like Kubernetes GOAT to simulate various attack scenarios, such as unauthorized access attempts and software tampering, to continuously test and improve your security measures.

## **Conclusion: Completing the Security Puzzle**

Securing your Kubernetes software supply chain might seem complex at first, but it becomes manageable when you approach it layer by layer. Just like solving a puzzle, each component—SBOMs, SLSA, and Sigstore—fits together to create a strong and unified security strategy. Each step you take intentionally builds upon the last, reinforcing your overall defense.

By learning from the broader security community and implementing these layered strategies, we can build robust security frameworks, not just for Kubernetes but for all modern systems. By sharing our knowledge and experiences, we collectively strengthen our defenses and move closer to achieving comprehensive and effective cloud-native security.

***

Beyond sharing knowledge here, I work directly with teams and organizations as **Nikkei One (n1)**—my solo consultancy focused on turning cloud-native ambitions into reality. Think of me as your one-stop shop. With expertise in Kubernetes, cloud security, and strategic tech leadership. Let’s collaborate to achieve your goals.

📬 **Reach out at** [**contact@nikkei.one**](mailto:contact@nikkei.one) to discuss consulting, hands-on training, or joint projects.

\
