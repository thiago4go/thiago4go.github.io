# Pod Security Standards (PSS): Baseline vs. Restricted Policies

Building a secure Kubernetes environment requires a strategic approach. Just like solving a Rubik's Cube, it can seem daunting at first, but with the right moves, you can align all the pieces. Kubernetes [Pod Security Standards (PSS)](https://kubernetes.io/docs/concepts/security/pod-security-standards/) are a crucial part of that strategy. In this article, we'll demystify PSS, focusing on the Baseline and Restricted policies, and how they work with Pod Security Admission Controllers to provide a layered defense. Join me as we explore how to achieve both security and agility in your Kubernetes deployments.

### Kubernetes Security: Building on Solid Foundations

Before we jump into PSS, let's quickly ground ourselves in the fundamentals. Cloud-native security isn't a single dimension; it's a **4C** framework, [you can read more about it here](https://cloud-native.nikkei.one/overview-of-cloud-native-security/cloud-native-security/understanding-the-4cs-of-cloud-native-security-a-layered-approach), each layer reinforcing the next, much like pieces on a Go board and Pod Security Standards are your tactical play at the **Container** and **Cluster** levels. They're the rules of engagement, standardized policies preventing privilege escalation and unauthorized access. Born from the evolution of Kubernetes, PSS emerged in v1.22, succeeding [PodSecurityPolicy (PSP)](https://kubernetes.io/docs/concepts/security/pod-security-policy/) to streamline and simplify how we bake security into our clusters.

## Meet the Security Trio

<figure><img src="../../.gitbook/assets/image.png" alt=""><figcaption><p>PSS and PSA</p></figcaption></figure>

PSS provides three distinct security profiles, each offering a progressively higher level of security. These profiles are designed to manage pod permissions.

1. **Privileged**: The least restrictive profile, allowing full access, including privilege escalation and host access. This is suitable for system-level tasks like debugging, monitoring tools, and service meshes that require elevated permissions.
2. **Baseline**: A moderate security profile that blocks privilege escalation and host-level settings but still allows containers to run as root. This is ideal for general-purpose workloads or legacy applications.
3. **Restricted**: The most secure profile, adhering to strict pod hardening practices. It blocks root containers, privilege escalation, and host access entirely, making it suitable for security-critical workloads.

Here’s a quick rundown, adapted from the official Kubernetes documentation, to visualize the policy differences:

<table data-header-hidden data-full-width="true"><thead><tr><th></th><th></th><th></th><th></th><th></th></tr></thead><tbody><tr><td><strong>Policy</strong></td><td><strong>Root Containers</strong></td><td><strong>Privilege Escalation</strong></td><td><strong>Host Access</strong></td><td><strong>Use Case</strong></td></tr><tr><td><strong>Privileged</strong></td><td>Allowed ✅</td><td>Allowed ✅</td><td>Full Access</td><td>System-level tasks (e.g., debugging)</td></tr><tr><td><strong>Baseline</strong></td><td>Allowed ✅</td><td>Blocked ❌</td><td>Limited</td><td>Legacy applications or general workloads</td></tr><tr><td><strong>Restricted</strong></td><td>Blocked ❌</td><td>Blocked ❌</td><td>None</td><td>Security-critical workloads</td></tr></tbody></table>

### Admission Controllers: Your Security Enforcers

Now, how do we actually _enforce_ these standards? Enter [**Pod Security Admission (PSA)**](https://kubernetes.io/docs/concepts/security/pod-security-admission/), Kubernetes’ built-in admission controller. PSA operates at the namespace level, giving you fine-grained control across your cluster. It scrutinizes every pod against your chosen PSS profile and reacts in one of three modes:

* ⛔ **Enforce:** "No entry!" – Non-compliant pods get blocked right at the gate.
* **📝 Audit:** "Let's keep an eye on this…" – Violations are logged, perfect for monitoring and catching drifts.
* ⚠️**Warn:** "Heads up!" – Users get alerts, a great way to educate and guide towards compliance.

## Deep Dive: Baseline vs. Restricted – Choosing Your Stance

### Baseline Policy:&#x20;

Baseline is your go-to for broad compatibility without sacrificing essential security. It’s like setting up guardrails on a highway – preventing major accidents without slowing down everyday traffic.

**Baseline – Key Restrictions :**

* No privileged containers allowed.
* Containers must run as non-root users.
* Host namespaces (PID, IPC) are off-limits .
* Linux capabilities get a sensible trim, blocking escalations.
* hostPath volumes? Nope.

**Baseline – The Upsides:**

* Plays well with almost everyone – 94% compatibility with common workloads.
* Smooth adoption, minimal friction – less operational headaches.
* Perfect starting line – essential security without breaking apps.

**Baseline – The Trade-offs:**

* Read-only hostPath… still a _tiny_ crack. Needs careful consideration for truly locked-down scenarios.

**Baseline in Action:** Think of a typical API service – needs to talk on the network, but no business poking around the host. Baseline fits perfectly.&#x20;

### Restricted Policy:&#x20;

Restricted is your security powerhouse. Think data vaults, high-security zones – environments where compromise is simply not an option.

**Restricted – Security Supercharges:**

* Non-root? _Mandatory_. No exceptions.
* Capabilities? Stripped down to the bare minimum – just NET\_BIND\_SERVICE.
* Seccomp? Strict enforcement with RuntimeDefault or custom profiles.
* Immutable filesystems – runtime image tampering? Not here.

**Restricted – The Impact:**

* Container breakouts are way down. Pair that with network policies, and you can seriously cut the risk of lateral movement.
* Notable considerations include necessary application modifications, such as the implementation of tmpfs for writable space. Additionally, ensuring compatibility with older applications may require further attention.

**Restricted in Action:** It means **compliance ready.** Payment processors, healthcare platforms – anyone handling super-sensitive data. Restricted is your compliance ally, aligning with frameworks like PCI-DSS, CIS Benchmarks, and NIST SP 800-190.

### Beyond Built-in: Exploring Alternative Enforcement Options

While Pod Security Admission (PSA) provides a fantastic built-in mechanism for enforcing these security standards, it's worth noting that the Kubernetes ecosystem offers other powerful alternatives for managing security profiles. Tools like  [Kyverno](https://kyverno.io/) and [OPA Gatekeeper](https://open-policy-agent.github.io/gatekeeper/website/docs/) provide different approaches and expanded capabilities for policy enforcement within your clusters.

The decision to leverage the built-in Pod Security Admission controller versus opting for a third-party tool is a strategic one, deeply intertwined with your specific environment and security philosophy. When evaluating any security solution, a critical factor is the trust you place in your supply chain. Ultimately, the most important takeaway is this: whether you choose the simplicity of the built-in PSA or the extended flexibility of tools like [Kyverno](https://kyverno.io/) or [OPA Gatekeeper](https://open-policy-agent.github.io/gatekeeper/website/docs/), adopting any robust enforcement approach is significantly better than neglecting pod security altogether.

## Building a Fortress: PSS in a Holistic Security Strategy

PSS isn't a silver bullet, but a cornerstone of layered security – like each strategically placed stone in a fortress wall. It’s strongest when integrated with other Kubernetes and cloud-native security tools:

**Security Arsenal Available to You:**

* **RBAC:** Least privilege access – control who does what, where.
* **Network Policies:** Segment your network – limit lateral movement with Calico, CNI policies.
* **Runtime Security (Falco):** Real-time threat detection – catch anomalies as they happen.
* **Image Scanning (Trivy):** Vulnerability scanning – find weaknesses _before_ deployment.
* **Policy Engines (Kyverno, OPA Gatekeeper):** Granular control, custom policies, automated remediation.
* **Service Mesh (Istio, Linkerd):** Defense-in-depth amplified – mTLS, traffic control, observability.

## **Strategic Deployment – Your PSS Migration Checklist**

* **Phase 1: Assessment and Planning:** This focuses on understanding your current state and preparing for the migration.
* **Phase 2: Implementation and Testing:** This covers the actual migration steps, including setting warn mode and moving to enforce mode.
* **Phase 3: Ongoing Operations and Optimization:** This addresses automation, monitoring, and handling exceptions.

### **Phase 1: Assessment and Planning**

**1.1: Initial Audit:**

Use `kubectl label ns <namespace> pod-security.kubernetes.io/audit=baseline --overwrite` (for a live cluster). Or `kubectl label --dry-run=server` (for a non-disruptive preview)

{% hint style="success" %}
Goal: Understandyour current pod security posture.
{% endhint %}

**1.2: Namespace Inventory:**

List all namespaces and categorize them based on sensitivity and application type.

{% hint style="success" %}
Goal: Identify namespaces that will require different PSS profiles.
{% endhint %}

**1.3: Define Target Profiles:**

Determine which PSS profile (Baseline, Restricted, Privileged) will be applied to each namespace group.

{% hint style="success" %}
_Goal:_ Establish a clear mapping between namespaces and security levels.
{% endhint %}

### **Phase 2: Implementation and Testing**

**2.1: Warn Mode Deployment:**

Apply `pod-security.kubernetes.io/warn` labels to namespaces, starting with less critical applications.

Example:

```yaml
apiVersion: v1
kind: Namespace
metadata:
    name: secure-app
    labels:
        pod-security.kubernetes.io/warn: restricted
        pod-security.kubernetes.io/warn-version: latest
```

{% hint style="success" %}
_Goal:_ Identify and address any compatibility issues _before_ enforcing the policies.
{% endhint %}

**2.2: Compatibility Testing (using `kubectl debug`):**

Use `kubectl debug` to test pod deployments against the target PSS profiles.

{% hint style="success" %}
_Goal:_ Ensure applications will function correctly under the stricter policies.
{% endhint %}

**2.3: Enforcement Rollout:**

Gradually switch from `warn` to `enforce` labels for each namespace group, starting with less critical applications.

Example:

```yaml
apiVersion: v1
kind: Namespace
metadata:
    name: secure-app
    labels:
        pod-security.kubernetes.io/enforce: restricted
        pod-security.kubernetes.io/enforce-version: latest
```

{% hint style="success" %}
_Goal:_ Implement PSS in a controlled and phased manner
{% endhint %}

### **Phase 3: Ongoing Operations and Optimization**

**3.1: Exception Handling:**

For legacy applications or special cases, use dedicated namespaces (Baseline or Privileged) or explore pod-level annotations (if applicable).

{% hint style="success" %}
_Goal:_ Accommodate exceptions while minimizing security risks.
{% endhint %}

**3.2 Automation (Kyverno/Gatekeeper):**

Implement Policy as Code using tools like Kyverno or Gatekeeper to automate namespace labeling, policy enforcement, and auto-correction. _Provide specific policy examples._

{% hint style="success" %}
_Goal:_ Ensure consistent and scalable PSS adoption.
{% endhint %}

**Continuous Monitoring:**

Monitor audit logs (`pod-security.kubernetes.io/audit: restricted`), Prometheus metrics, and Kubernetes audit logs for violations and unexpected behavior.&#x20;

{% hint style="success" %}
_Goal:_ Maintain a secure posture and proactively address any issues.
{% endhint %}

## OS consideration

When deploying to a mixed Linux/Windows Kubernetes cluster, remember that pod `SecurityContext` settings primarily target Linux. This means that the security mechanisms you rely on for Linux pods might [not translate directly to Windows](https://kubernetes.io/docs/concepts/windows/intro/#compatibility-v1-pod-spec-containers-securitycontext). You'll need to explore different strategies to secure your Windows-based applications.

## Conclusion: Your Kubernetes Security Journey Starts Now

Kubernetes Pod Security Standards aren't just another feature – they're a fundamental shift towards secure-by-default cloud-native infrastructure. From the pragmatic Baseline to the robust Restricted policy, PSS provides the structure and tooling to enforce critical security measures at the pod level.

As I refine these strategies through real-world research and community feedback, one thing is clear: while Baseline is a fantastic starting point, the industry is leaning decisively towards **Restricted as the gold standard**. ([Google ](https://cloud.google.com/kubernetes-engine/enterprise/policy-controller/docs/how-to/using-pss-restricted)and [Flux](https://fluxcd.io/blog/2022/03/security-pod-security-standard-restricted/)). By embracing PSS, layering it with complementary security tools, and adopting a proactive, strategic mindset, you're not just patching vulnerabilities – you're building a truly resilient and agile Kubernetes environment.

Kubernetes security, like a Rubik's Cube, might seem complex. But with each layer you master – each policy you enforce, each tool you integrate – you move closer to that "solved" state: a secure, robust, and dynamic cloud-native platform.\
\
Beyond sharing knowledge here, I work directly with teams and organizations as Nikkei One (n1) — As a solo consultancy, I specialize in guiding organizations through the complexities of cloud-native security, offering hands-on expertise to ensure your Kubernetes environments are not just running, but running securely. Whether you're aiming for the essential protections of the Baseline policy or the robust defenses of Restricted, I can help you. Let’s collaborate to achieve your goals.\
\
📬 Reach out at contact@nikkei.one to discuss consulting, hands-on training, or joint projects.\
\
The journey to Kubernetes security mastery is continuous. Let’s keep learning, keep building, and keep securing our cloud-native world, together!\


