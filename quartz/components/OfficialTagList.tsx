import { FullSlug, resolveRelative, slugTag } from "../util/path"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"

const OfficialTagList: QuartzComponent = ({ fileData, displayClass }: QuartzComponentProps) => {
  const tags = fileData.frontmatter?.officialTags
  if (!tags || tags.length === 0) return null

  return (
    <section
      class={classNames(displayClass, "official-opinion-tags")}
      aria-label="Official opinion tags"
    >
      <p class="official-opinion-tags-label">Official opinion tags</p>
      <ul>
        {tags.map((tag) => {
          const linkDest = resolveRelative(
            fileData.slug!,
            `tags/opinion/${slugTag(tag)}` as FullSlug,
          )
          return (
            <li>
              <a href={linkDest} class="internal official-opinion-tag-link">
                {tag}
              </a>
            </li>
          )
        })}
      </ul>
    </section>
  )
}

OfficialTagList.css = `
.official-opinion-tags {
  margin: 0.25rem 0 1.25rem;
}

.official-opinion-tags-label {
  color: var(--darkgray);
  font-family: var(--headerFont);
  font-size: 0.82rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  margin: 0 0 0.45rem;
  text-transform: uppercase;
}

.official-opinion-tags > ul {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  list-style: none;
  margin: 0;
  padding: 0;
}

.official-opinion-tags > ul > li {
  display: inline-block;
  margin: 0;
}

a.internal.official-opinion-tag-link {
  background-color: var(--highlight);
  border: 1px solid color-mix(in srgb, var(--secondary) 28%, transparent);
  border-radius: 999px;
  display: inline-block;
  font-family: var(--bodyFont);
  font-size: 0.88rem;
  line-height: 1.3;
  padding: 0.2rem 0.55rem;
}
`

export default (() => OfficialTagList) satisfies QuartzComponentConstructor
