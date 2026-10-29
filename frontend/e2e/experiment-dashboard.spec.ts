import { expect, test } from '@playwright/test'

const sequence = 'ACDEFGHIKLMN'
const sequences = Array.from({ length: 20 }, () => sequence).join('\n')

test.beforeEach(async ({ page }) => {
  await page.route('**/api/v1/experiments?*', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        items: [],
        total: 0,
        limit: 5,
        offset: 0,
      }),
    })
  })
    await page.goto('/')
})

test('displays the experiment dashboard', async ({ page }) => {
  await expect(
    page.getByRole('heading', { name: 'Create Experiment' }),
  ).toBeVisible()

  await expect(
    page.getByRole('heading', { name: 'Experiments' }),
  ).toBeVisible()

  await expect(page.getByText('No experiments yet.')).toBeVisible()
})

test('validates required fields', async ({ page }) => {
  await page.getByRole('button', {
    name: 'Create Experiment',
  }).click()

  await expect(
    page.getByText('Experiment name is required'),
  ).toBeVisible()
})

test('validates the number of sequences', async ({ page }) => {
  await page.getByLabel('Experiment Name').fill('Test experiment')
  await page.getByLabel('Protein Sequences').fill(sequence)

  await page.getByRole('button', {
    name: 'Create Experiment',
  }).click()

  await expect(page.getByText('Enter exactly 20 sequences')).toBeVisible()
})

test('creates an experiment using lowercase comma-separated manual entry', async ({ page }) => {
  let created = false
  const lowercaseSequences = sequences.replaceAll('\n', ', ').toLowerCase()

  await page.route('**/api/v1/experiments', async (route) => {
    if (route.request().method() !== 'POST') {
      await route.fallback()
      return
    }

    const request = route.request().postDataJSON()

    expect(request).toEqual({
      name: 'Kinase screening',
      sequences: Array.from({ length: 20 }, () => sequence),
    })

    created = true

    await route.fulfill({
      status: 201,
      contentType: 'application/json',
      body: JSON.stringify({
        id: '123e4567-e89b-12d3-a456-426614174000',
        name: request.name,
        sequences: request.sequences,
        created_at: '2026-10-28T10:00:00Z',
      }),
    })
  })

  await page.getByLabel('Experiment Name').fill('Kinase screening')
  await page.getByLabel('Protein Sequences').fill(lowercaseSequences)

  await expect(page.getByText('20 / 20')).toBeVisible()

  await page.getByRole('button', {
    name: 'Create Experiment',
  }).click()

  await expect.poll(() => created).toBe(true)
  await expect(page.getByRole('status')).toHaveText('Experiment created successfully')
  await expect(page.getByLabel('Experiment Name')).toHaveValue('')
  await expect(page.getByLabel('Protein Sequences')).toHaveValue('')
})

test('shows a backend error', async ({ page }) => {
  await page.route('**/api/v1/experiments', async (route) => {
    if (route.request().method() !== 'POST') {
      await route.fallback()
      return
    }

    await route.fulfill({
      status: 422,
      contentType: 'application/json',
      body: JSON.stringify({
        error: 'Invalid protein sequence',
      }),
    })
  })

  await page.getByLabel('Experiment Name').fill('Invalid experiment')
  await page.getByLabel('Protein Sequences').fill(sequences)
  await page.getByRole('button', { name: 'Create Experiment' }).click()

  await expect(page.getByRole('alert')).toContainText(
    'Invalid protein sequence',
  )
})


test('displays existing experiments', async ({ page }) => {
  const longName = 'Kinase screening experiment with a deliberately long descriptive name'

  await page.route('**/api/v1/experiments?*', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        items: [{
          id: '123e4567-e89b-12d3-a456-426614174000',
          name: longName,
          sequences: Array.from({ length: 20 }, () => sequence),
          created_at: '2026-10-28T10:00:00Z',
        }],
        total: 1,
        limit: 5,
        offset: 0,
      }),
    })
  })

  await page.goto('/')

  await expect(page.getByRole('table', { name: 'Experiments' })).toBeVisible()
  await expect(page.getByText('Kinase screening experiment with a deliberately...')).toBeVisible()
  await expect(page.getByRole('cell', { name: `Experiment name: ${longName}` })).toBeVisible()
  await expect(page.getByText('Showing 1 to 1 of 1 experiments')).toBeVisible()
})

test('clears the form', async ({ page }) => {
  const name = page.getByLabel('Experiment Name')
  const sequenceInput = page.getByLabel('Protein Sequences')

  await name.fill('Kinase screening')
  await sequenceInput.fill(sequences)
  await page.getByRole('button', { name: 'Clear' }).click()

  await expect(name).toHaveValue('')
  await expect(sequenceInput).toHaveValue('')
  await expect(page.getByText('0 / 20')).toBeVisible()
})

test('shows an error when experiments cannot be loaded', async ({ page }) => {
  await page.route('**/api/v1/experiments?*', async (route) => {
    await route.fulfill({
      status: 500,
      contentType: 'application/json',
      body: JSON.stringify({ detail: 'Server error' }),
    })
  })

  await page.goto('/')

  await expect(page.getByText('Could not load experiments')).toBeVisible()
})

test('loads the next experiments page', async ({ page }) => {
  const requestedOffsets: string[] = []

  await page.route('**/api/v1/experiments?*', async (route) => {
    const url = new URL(route.request().url())
    const offset = url.searchParams.get('offset') ?? '0'
    requestedOffsets.push(offset)

    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        items: [],
        total: 10,
        limit: 5,
        offset: Number(offset),
      }),
    })
  })

  await page.goto('/')
  await page.getByRole('button', { name: 'Next page' }).click()

  await expect.poll(() => requestedOffsets).toContain('5')
})

test('changes the number of experiments shown per page', async ({ page }) => {
  const requestedLimits: string[] = []

  await page.route('**/api/v1/experiments?*', async (route) => {
    const url = new URL(route.request().url())
    const limit = url.searchParams.get('limit') ?? '5'
    requestedLimits.push(limit)

    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ items: [], total: 50, limit: Number(limit), offset: 0 }),
    })
  })

  await page.goto('/')
  await page.getByLabel('Rows per page').selectOption('25')

  await expect.poll(() => requestedLimits).toContain('25')
  await expect(page.getByLabel('Rows per page')).toHaveValue('25')
})


test('uploads a FASTA file', async ({ page }) => {
  let uploaded = false

  await page.route('**/api/v1/experiments/upload', async (route) => {
    uploaded = true

    expect(route.request().postData()).toContain('FASTA screening')
    expect(route.request().postData()).toContain('valid.fasta')

    await route.fulfill({
      status: 201,
      contentType: 'application/json',
      body: JSON.stringify({
        id: '123e4567-e89b-12d3-a456-426614174000',
        name: 'FASTA screening',
        sequences: Array.from({ length: 20 }, () => sequence),
        created_at: '2026-10-28T10:00:00Z',
      }),
    })
  })

  await page.getByLabel('Experiment Name').fill('FASTA screening')
  await page.getByRole('tab', { name: 'Upload FASTA' }).click()
  await page.getByLabel('Choose a FASTA file').setInputFiles(
    'e2e/fixtures/valid.fasta',
  )

  await expect(page.getByText('valid.fasta')).toBeVisible()
  await page.getByRole('button', { name: 'Create Experiment' }).click()

  await expect.poll(() => uploaded).toBe(true)
  await expect(page.getByRole('status')).toHaveText('FASTA experiment uploaded successfully')
  await expect(page.getByLabel('Experiment Name')).toHaveValue('')
  await expect(page.getByText('valid.fasta')).not.toBeVisible()
})

test('shows the API error when a FASTA upload fails', async ({ page }) => {
  await page.route('**/api/v1/experiments/upload', async (route) => {
    await route.fulfill({
      status: 413,
      contentType: 'application/json',
      body: JSON.stringify({ error: 'File too large' }),
    })
  })

  await page.getByLabel('Experiment Name').fill('FASTA screening')
  await page.getByRole('tab', { name: 'Upload FASTA' }).click()
  await page.getByLabel('Choose a FASTA file').setInputFiles(
    'e2e/fixtures/valid.fasta',
  )
  await page.getByRole('button', { name: 'Create Experiment' }).click()

  await expect(page.getByRole('alert')).toHaveText('File too large')
})
